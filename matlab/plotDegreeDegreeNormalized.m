function plotDegreeDegreeNormalized(netType, lthreshold, hthreshold, titleStr)
    thresholds = [0];
    %maxDegree = 0;
    for i=1:numel(thresholds)
        plotEdgeWtsAcrossCuisines('cooc', thresholds(i),lthreshold, hthreshold, titleStr);
        %maxDegree = plotCuisine('cooc', thresholds(i), maxDegree);
    end
end
function plotEdgeWtsAcrossCuisines(netType, threshold, lthreshold, hthreshold, titleStr)
    plotTitle = strcat(titleStr, '-EdgeDistributions-', num2str(threshold), '-', num2str(lthreshold), ':', num2str(hthreshold));
    allEdgeDist = {};
    cuisines = {'indian', 'italian', 'mexican', 'spanish', 'chinese', 'french'};
    for i=1:numel(cuisines)
        cuisine = cuisines{i};
        [data, node, nodeDegrees] = getCuisineData(cuisine, netType, threshold );
        if numel(data)> 1
            allEdgeDist{i} = data(:,3);
            maxEdgeWt = max(data(:,3));
            allEdgeDist{i} = allEdgeDist{i};%/maxEdgeWt;
        end
    end
    h = figure;
    col = lines(10);
    for i=1:numel(allEdgeDist)
        sortedList = sort(allEdgeDist{i}, 'descend');
        candidates = sortedList;
        if lthreshold < numel(sortedList) 
            if hthreshold < numel(sortedList)
                candidates = sortedList(lthreshold:hthreshold, :);
            else
                candidates = sortedList(lthreshold:numel(sortedList), :);
            end
            loglog(candidates, '.', 'color',col(i,:));
            hold on;
        else
            %do nothing. 
        end

    end
    legend(cuisines);
    title(plotTitle);
    print(h, '-dpng', strcat(plotTitle, '.png'));
end
function maxDegree = plotCuisine(netType, threshold, inMaxDegree)
    allEdgeDist = {};
    nodeCounts = [];
    plotTitle = strcat('Degree-DegreePlot-PruneNet-Normalized-', num2str(threshold));
    cuisines = {'indian', 'italian', 'chinese', 'french', 'spanish', 'mexican'};
    maxDegree = inMaxDegree;
    matData = {};
    rCount = zeros(numel(cuisines),1);
    for i=1:numel(cuisines)
        cuisine = cuisines{i};
        [data, node, nodeDegrees] = getCuisineData(cuisine, netType, threshold );
        if numel(data) > 1
            allEdgeDist{i} = data;
            nodeCounts = [nodeCounts, numel(node)];
        else
            nodeCounts = [nodeCounts, 0];
        end
        if threshold == 0
            td = max(max(data(:,1)), max(data(:,2)));
            if td > maxDegree
                maxDegree = td;
            end
        end
        if numel(data) > 1 && threshold > 0
            [matrix, rCount] = getMatFormMatrix(data, inMaxDegree, nodeCounts(i));
            matData{i} = matrix;
            ind = find(rCount~=0);
            if( numel(ind) > 0 )
                rCountAll(i) = max(ind);
            else 
                rCountAll(i) = 0;
            end
        end
    end
    if threshold > 0
        for i=1:numel(cuisines)
            cuisine = cuisines{i};
            matrix = matData{i};
            if (size(matrix,1) > 0) 
                maxRowCount = max(rCountAll);
                if maxRowCount > 0
                    subplotTitle = strcat(plotTitle, '-', cuisine, '-normalizedMat');
                    h = figure;
                    colormap(hot);
                    imagesc(matrix(1:maxRowCount, 1:maxRowCount));
                    title(subplotTitle);
                    print(h, '-dpng', strcat(subplotTitle, '.png'));
                    close(h);
                    save(strcat(subplotTitle, '.mat'), 'matrix', 'node', 'nodeDegrees', 'data'); 
                end
            end
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
        degData = [nodeDegrees(k(1))/numel(node), nodeDegrees(k(2))/numel(node), k(3)];
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
function [mat, c] = getMatFormMatrix(data, maxDegree, nodeCount)
    mat = zeros(1000, 1000);
    for i=1:size(data,1)
        x = data(i,1);
        y = data(i,2);
        xInd = ceil((x*1000)/maxDegree);
        yInd = ceil((y*1000)/maxDegree);
        if xInd > 1000 || yInd > 1000
            continue;
        end
        mat(xInd,yInd) = mat(xInd,yInd) + (1/nodeCount);
    end
    c = zeros(1000,1);
    for i=1:1000
        c(i) = numel(find(mat(i,:) ~=0));
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
