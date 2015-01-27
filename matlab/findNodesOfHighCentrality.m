function findNodesOfHighCentrality()
    cuisines = {'indian', 'chinese', 'mexican', 'spanish', 'french', 'italian'};
    metric = {'avgNeigDegree', 'degreeCentrality', 'betCentrality', 'closeness', 'eigenvectorCentrality', 'communicability', 'clusCoeff'};
    sortedIndices = cell(numel(cuisines), numel(metric));
    diffInNodes = cell(numel(cuisines),1);
    nodesInCuisines = cell(numel(cuisines), 1);
    for i=1:numel(cuisines)
        load(strcat(cuisines{i},'_cooc.mat'));
        diffInNodes{i} = cell(numel(metric), numel(metric));
        
        for j=1:numel(metric)
            eval(sprintf('x=metric{1,%d};', j));
            x = eval(x);
            [sortedX, sortedXIndices] = sort(x, 'descend');
            sortedIndices{i,j} = sortedXIndices;
        end
        for j=1:numel(metric)
            for k=1:numel(metric)
                if j~=k
                    temp = sortedIndices{i,j} == sortedIndices{i,k};
                    diffInNodes{i}{j,k} = find(temp == 1);
                end
            end
        end
        nodesInCuisines{i} = node;
    end
    save('CentralityData.mat','diffInNodes', 'sortedIndices', 'nodesInCuisines');
    
end