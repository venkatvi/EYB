function plotDegreeDegree(netType, edgeThreshold )
    cuisines = {'indian', 'chinese', 'mexican', 'spanish',  'italian', 'french'};
    
    for i=1:6
        figure;
        colormap(hot);
        data = getCuisineData(cuisines{i}, netType, edgeThreshold);
        imagesc(data);
        xlabel(cuisines{i});
        title(strcat('Degree Degree Plot - ', cuisines{i}));
    end
end
function degreeDegreeMat = getCuisineData(cuisine, netType, edgeThreshold)
    edgWtFile = strcat(cuisine , '_' , netType , '_wtDist.csv');
    nodeMetricsFile = strcat(cuisine, '_', netType, '_nodeMetrics.csv');
    [src, dest, wt] =  loadFile(edgWtFile);
    [node, degree] = loadFile(nodeMetricsFile);
    
    oldDeg = zeros(numel(degree),1);
    for i=1:numel(degree)
        oldDeg(i) = str2double(degree{i});
    end
    
%    newDeg = zeros(numel(node), 1);
    
    maxDeg = max(oldDeg);
    degreeDegreeMat = zeros(maxDeg, maxDeg);
    
%    data = [];
    [wt, orderedIndices] = sort(wt, 'descend');
    for i=1:edgeThreshold
        eWt = wt(i); %percent of all recipes in which this edge occurs
        s = src(orderedIndices(i));
        sind = find(ismember(node, s) ==1);     
        
        d = dest(orderedIndices(i));
        dind = find(ismember(node, d)==1);
        
        if sind ~= dind
%             newDeg(sind) = newDeg(sind) + 1;
%             newDeg(dind) = newDeg(dind) + 1;
%             k = [sind, dind, eWt];
%             data = [data; k];
            degreeDegreeMat(oldDeg(sind), oldDeg(dind)) = degreeDegreeMat(oldDeg(sind), oldDeg(dind)) + 1;
        end
    end
    
%     diff = oldDeg-newDeg;
%     ind = find(diff > 0);
%     if numel(ind) > 0
%         j = 1;
%     end
end
