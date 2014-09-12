function plotDegreeDegree(netType, edgeThreshold )
    cuisines = {'indian', 'chinese', 'mexican', 'spanish',  'italian', 'french'};
    cuisineText = {'Indian', 'Chinese', 'Mexican', 'Spanish', 'Italian', 'French'};
    origDegreeDegreeAllCuisines = cell(6,1);
    prunedDegreeDegreeAllCuisines = cell(6,1);
    ingredCountInCore = zeros(6,1);
    maxDegree = zeros(6,1);
    for i=1:6
        [origDegreeDegreeAllCuisines{i}, prunedDegreeDegreeAllCuisines{i}, maxDegree(i), ingredCountInCore(i)] = getCuisineData(cuisines{i}, netType, edgeThreshold);
    end
    maxOfAllDegrees = max(maxDegree);
    for i=1:6
         prunedData = prunedDegreeDegreeAllCuisines{i}; 
         olddim = size(prunedData, 1);
         prunedData = appendExtraColumnsIfRequired(maxOfAllDegrees, prunedData);
         h = figure;
         colormap(hot);
         imagesc(prunedData);
         title(strcat('Degree Degree Plot - ', cuisines{i}, '-', num2str(edgeThreshold), 'links'));
         xlabel(strcat('Nodes:', num2str(ingredCountInCore(i)), '; MaxDegree:', num2str(maxDegree(i))));
         fileName = strcat('DegreeDegree', cuisineText{i}, num2str(edgeThreshold));
         saveas(h, fileName, 'png');
   end
        
end
function newData = appendExtraColumnsIfRequired(maxDegree, data)
    olddim =size(data, 1);
    if maxDegree > olddim
        newData = zeros(maxDegree, maxDegree);
        newData(1:olddim, 1:olddim) = data(1:olddim, 1:olddim);
    else
        newData = data;
    end
end

function [degreeDegreeMat, degreeDegreePrunedMat, maxDegree, nodeCount] = getCuisineData(cuisine, netType, edgeThreshold)
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
    nodeDegreeContainer = containers.Map(char('a'), int32(0));
    edgeContainer = containers.Map(char('a'), ?handle);
%    data = [];
    [wt, orderedIndices] = sort(wt, 'descend');
    for i=1:edgeThreshold
        eWt = wt(i); %percent of all recipes in which this edge occurs
        s = src(orderedIndices(i));
        if nodeDegreeContainer.isKey(s{1})
            nodeDegreeContainer(s{1}) = nodeDegreeContainer(s{1}) + 1;
        else
            nodeDegreeContainer(s{1}) = 1;
        end
        sind = find(ismember(node, s{1}) ==1);     
        
        d = dest(orderedIndices(i));
        if nodeDegreeContainer.isKey(d{1})
            nodeDegreeContainer(d{1}) = nodeDegreeContainer(d{1}) + 1;
        else
            nodeDegreeContainer(d{1}) = 1;
        end
        dind = find(ismember(node, d{1})==1);
        
        if edgeContainer.isKey(s{1})
            destEdges = edgeContainer(s{1});
            if ~isempty(destEdges)
                destEdges{numel(destEdges) + 1} = d{1};
            else
                destEdges{1} = d{1};
            end
            edgeContainer(s{1}) = destEdges;
        else
            destEdges{1} = d{1};
            edgeContainer(s{1}) = destEdges;
        end
        
        if sind ~= dind
%             newDeg(sind) = newDeg(sind) + 1;
%             newDeg(dind) = newDeg(dind) + 1;
%             k = [sind, dind, eWt];
%             data = [data; k];
            degreeDegreeMat(oldDeg(sind), oldDeg(dind)) = degreeDegreeMat(oldDeg(sind), oldDeg(dind)) + 1;
            degreeDegreeMat(oldDeg(dind), oldDeg(sind)) = degreeDegreeMat(oldDeg(dind), oldDeg(sind)) + 1;
        end
    end
    nodeDegreeContainer.remove('a');
    edgeContainer.remove('a');
    degrees = nodeDegreeContainer.values;
    degrees = cell2mat(degrees);
    maxDegree = max(degrees);
    degreeDegreePrunedMat = zeros(maxDegree, maxDegree);
    keys = edgeContainer.keys;
    for i=1:length(keys)
        s = keys{i};
        sdeg = nodeDegreeContainer(s);
        dest = edgeContainer(s);
        for j=1:length(dest)
            d = dest{j};
            ddeg = nodeDegreeContainer(d);
            degreeDegreePrunedMat(sdeg, ddeg) = degreeDegreePrunedMat(sdeg, ddeg) + 1;
            degreeDegreePrunedMat(ddeg, sdeg) = degreeDegreePrunedMat(ddeg, sdeg) + 1;
        end
    end
    nodeCount = int32(nodeDegreeContainer.Count);
    
%     diff = oldDeg-newDeg;
%     ind = find(diff > 0);
%     if numel(ind) > 0
%         j = 1;
%     end
end
