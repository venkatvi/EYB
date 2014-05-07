function plotDegreeDegreeNetPrune(netType)
    thresholds = [0, 0.0001, 0.0005, 0.001, 0.005, 0.01, 0.05, 0.1, 0.2, 0.3];
%     plotCuisine('indian', netType, threshold);
%     plotCuisine('italian', netType, threshold);
%     plotCuisine('spanish', netType, threshold);
%     plotCuisine('mexican', netType, threshold);
%     plotCuisine('chinese', netType, threshold);
%     plotCuisine('french', netType, threshold);
    for i=1:numel(thresholds)
        %plotEdgeWtsAcrossCuisines('cooc', thresholds(i));
        plotCuisine('cooc', thresholds(i))
    end
end
function plotEdgeWtsAcrossCuisines(netType, threshold)
    plotTitle = strcat('EdgeDistributions-', num2str(threshold));
    allEdgeDist = {};
    cuisines = {'indian', 'italian', 'mexican', 'spanish', 'chinese', 'french'};
    for i=1:numel(cuisines)
        cuisine = cuisines{i};
        [data, node, nodeDegrees] = getCuisineData(cuisine, netType, threshold );
        if numel(data)> 1
            allEdgeDist{i} = data(:,3);
        end
    end
    h = figure;
    col = lines(10);
    for i=1:numel(allEdgeDist)
        loglog(sort(allEdgeDist{i},'descend'), '.', 'color',col(i,:));
        hold on;
    end
    legend(cuisines);
    title(plotTitle);
    print(h, '-dpng', strcat(plotTitle, '.png'));
end
function plotCuisine(netType, threshold)
    allEdgeDist = {};
    nodeCounts = [];
    plotTitle = strcat('Degree-DegreePlot-PruneNet-', num2str(threshold));
    cuisines = {'indian', 'italian', 'chinese', 'french', 'spanish', 'mexican'};
    for i=1:numel(cuisines)
        cuisine = cuisines{i};
        [data, node, nodeDegrees] = getCuisineData(cuisine, netType, threshold );
        if numel(data) > 1
            allEdgeDist{i} = data;
            nodeCounts = [nodeCounts, numel(node)];
        else
            nodeCounts = [nodeCounts, 0];
        end
    end
    [scaleUpMultiple, maxDegree] = getScaleUpFactor(allEdgeDist);
    scaleUpMultiple = ones(1, 6);
    for i=1:numel(cuisines)
        cuisine = cuisines{i};
        data = allEdgeDist{i};
        if numel(data) > 0
            %maxDegree = max(max(data(:,1)),max(data(:,2)) );
            %scaleUp = scaleUpMultiple /maxDegree;
            data(:,1) = data(:,1)*scaleUpMultiple(i);
            data(:,2) = data(:,2)*scaleUpMultiple(i);
            matrix = getMatrixNormalized(data, nodeCounts(i));
            %matrix = getMatrixNormalized(data, maxDegree, nodeCounts(i));
            subplotTitle = strcat(plotTitle, '-', cuisine, '-normalized');
            h = figure;
            colormap('hot');
            %imagesc(matrix);
            plot(mat(:,1), mat(:,2), '.', 'markerfacecolor',[1 1 1]*greyscale(i));
            title(subplotTitle);
            print(h, '-dpng', strcat(subplotTitle, '.png'));
            close(h);
            save(strcat(subplotTitle, '.mat'), 'matrix', 'node', 'nodeDegrees', 'data'); 
        end
    end
    %close(h);    
end
function [scaleUpMultiple, maxOfDegrees] = getScaleUpFactor(allData)
    degrees =[];
    for i=1:numel(allData)
        data = allData{i};
        if numel(data) > 0
            maxDegree = max(max(data(:,1)), max(data(:,2)));
        else 
            maxDegree = 1;
        end
        degrees = [degrees maxDegree];
    end
    %scaleUpMultiple = lcm(degrees(1), lcm(degrees(2), lcm(degrees(3), lcm(degrees(4), lcm(degrees(5), degrees(6))))));
    maxOfDegrees = max(degrees);
    scaleUpMultiple  = maxOfDegrees ./degrees;
end
function [data, node, nodeDegrees] = getCuisineData(cuisine, netType, threshold)
    edgWtFile = strcat(cuisine , '_' , netType , '_wtDist.csv');
    nodeMetricsFile = strcat(cuisine, '_', netType, '_nodeMetrics.csv');
    [src, dest, wt] =  loadFile(edgWtFile);
    [node, degree] = loadFile(nodeMetricsFile);
    
    minWt = min(wt);
    maxWt = max(wt);
        
    d = zeros(numel(degree),1);
    for i=1:numel(degree)
        d(i) = str2double(degree{i});
    end
         
    prunedNodeDegrees = d;
    data = [];
    edgesC = 0;
    [wt, ind] = sort(wt);
    src = src(ind);
    dest = src(ind);
    nodeDegrees = zeros(numel(node), 1);
    loops = 0;
    prunedNetSrcDest = [];
    for i=1:numel(wt)
        eWt = wt(i); %percent of all recipes in which this edge occurs
        
        s = src(i);
        sind = find(ismember(node, s) ==1);

        d = dest(i);
        dind = find(ismember(node, d)==1);
        
        
        if eWt >= threshold
            if(sind == dind)
                loops = loops + 1;
            else
                nodeDegrees(sind) = nodeDegrees(dind) + 1;
                nodeDegrees(dind) = nodeDegrees(dind) + 1;
                k = [sind,dind, eWt];
                prunedNetSrcDest = [prunedNetSrcDest; k];
            end
        end
    end
    for i=1:size(prunedNetSrcDest,1)
        k = prunedNetSrcDest(i,:);
        degData = [nodeDegrees(k(1))/numel(node), nodeDegrees(k(2))/numel(node), k(3)/numel(node)];
        data = [data; degData];
    end
end
function mat = getMatrixNormalized(data, nodeCount)
    mat = [];
    for i=1:size(data,1)
        x = data(i,1);
        y = data(i,2);
        if ~isempty(mat)
            xInd = find(mat(:,1)==x);
        else
            xInd = [];
        end
        if ~isempty(xInd)
            subsets = mat(xInd, :);
            yInd = find(subsets(:,2)==y);
            if ~isempty(yInd)
                subSetIndex = yInd(1);
                origIndex = xInd(subSetIndex);
                mat(origIndex, 3) = mat(origIndex, 3) + 1;
            else
                mat = [mat; x, y, 1];
            end
        else
            mat = [mat; x, y, 1];
        end
    end
    for i=1:size(mat, 1)
        mat(i, 3) = mat(i, 3)/nodeCount;
    end
            
end
function mat = getMatrix(data, scaleUp, nodeCount)
    mat = zeros(scaleUp, scaleUp);
    for i=1:size(data,1)
        x = ceil(data(i,1));
        y = ceil(data(i,2));
        mat(x,y) = mat(x,y) + 1;
    end
    for i=1:numel(data(:,1))
        x = ceil(data(i,1));
        y = ceil(data(i,2));
        mat(x,y) = mat(x,y)/nodeCount;
    end
end