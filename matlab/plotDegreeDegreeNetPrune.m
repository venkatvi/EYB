function plotDegreeDegreeNetPrune(netType, threshold )
    plotCuisine('indian', netType, threshold);
    plotCuisine('italian', netType, threshold);
    plotCuisine('spanish', netType, threshold);
    plotCuisine('mexican', netType, threshold);
    plotCuisine('chinese', netType, threshold);
    plotCuisine('french', netType, threshold);
end
function plotCuisine(cuisine, netType, threshold)
    plotTitle = strcat('Degree-DegreePlot-PruneNet-', num2str(threshold));
    [data, node, nodeDegrees] = getCuisineData(cuisine, netType, threshold );
    if numel(data) > 1
        matrix = getMatrix(data);
        subplotTitle = strcat(plotTitle, '-', cuisine);
        h = figure;
        colormap('hot');
        imagesc(matrix);
        title(subplotTitle);
        print(h, '-dpng', strcat(subplotTitle, '.png'));
        close(h);
        
        h = figure;
        subplot(1,2,1);
        loglog(sort(data(:,3),'descend'), '.');
        xlabel('edgeDistribution');
        subplot(1,2,2);
        indn = find(nodeDegrees~=0);
        n = nodeDegrees(indn);
        loglog(sort(n, 'descend'), '.');
        xlabel('nodeDegreeDistribution');
        print(h, '-dpng', strcat(subplotTitle, '-dist-loglog.png'));
        close(h);
        
        
        h = figure;
        subplot(1,2,1);
        plot(sort(data(:,3),'descend'), '.');
        xlabel('edgeDistribution');
        subplot(1,2,2);
        indn = find(nodeDegrees~=0);
        n = nodeDegrees(indn);
        plot(sort(n, 'descend'), '.');
        xlabel('nodeDegreeDistribution');
        print(h, '-dpng', strcat(subplotTitle, '-dist.png'));
        close(h);
        
        save(strcat(subplotTitle, '.mat'), 'matrix', 'node', 'nodeDegrees', 'data'); 
    end
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
        degData = [nodeDegrees(k(1)), nodeDegrees(k(2)), k(3)];
        data = [data; degData];
    end
    
   data
end
function mat = getMatrix(data)
    maxDeg = max(max(data(:,1)), max(data(:,2)));
    mat = zeros(maxDeg, maxDeg);
    for i=1:size(data,1)
        mat(data(i,1), data(i,2)) = mat(data(i,1), data(i,2)) + 1;
    end
end
