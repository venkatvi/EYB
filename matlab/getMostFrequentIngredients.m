function getMostFrequentIngredients(numEdges, mode)
    cuisines = {'indian', 'chinese', 'mexican', 'spanish', 'italian', 'french'};
    frequentIngredients = cell(6,4);
    
    for i=1:6
        fileName1 = strcat(cuisines{i}, '_cooc.mat');
        load(fileName1);
        
        [sortedDegree, sortedIndices] = sort(degree, 'descend');
        sortedNodeNames = node(sortedIndices);
        topFrequentIngredients{i, 1} = sortedNodeNames;
        
        fileName2 = strcat(cuisines{i}, '_edge_wts.mat');
        load(fileName2);
        [sortedCooccurrence, sortedIndices] = sort(cooc, 'descend');
        sortedIngred1 = ingred1(sortedIndices);
        sortedIngred2 = ingred2(sortedIndices);
       
        sortedIngreds = containers.Map(char('a'), int32(0));
        for i1=1:numEdges
            if (sortedIngreds.isKey(sortedIngred1{i1}))
                sortedIngreds(sortedIngred1{i1}) = sortedIngreds(sortedIngred1{i1}) + 1;
            else
                sortedIngreds(sortedIngred1{i1}) = 1;
            end
            if (sortedIngreds.isKey(sortedIngred2{i1}))
                sortedIngreds(sortedIngred2{i1}) = sortedIngreds(sortedIngred2{i1}) + 1;
            else
                sortedIngreds(sortedIngred2{i1}) = 1;
            end
        end
        temp = sortedIngreds.values;
        sortedIngredsFrequency = zeros(numel(temp), 1);
        for i1=1:numel(temp)
            sortedIngredsFrequency(i1) = temp{i1};
        end
        [sortedFrequencies, sortedIndices] = sort(sortedIngredsFrequency, 'descend');
        sortedIngredKeys = sortedIngreds.keys;
        sortedIngreds = sortedIngredKeys(sortedIndices);
        
        topDegree = sortedDegree(1:numel(sortedIngreds)-1);
        topIngreds = sortedNodeNames(1:numel(sortedIngreds)-1);
        
        
        frequentIngredients{i,1} = sortedIngreds(1:numel(sortedIngreds)-1)';
        frequentIngredients{i,2} = sortedFrequencies(1:numel(sortedIngreds)-1);
        frequentIngredients{i,3} = topIngreds;
        frequentIngredients{i,4} = topDegree;
    end
    
    save('frequentIngreds.mat', 'frequentIngredients');
    figure;
    colorIndex = [1, 8, 25, 40, 56, 64]; 
    c = colormap(jet);
    for i=1:6
        if strcmp(mode, 'log')
            loglog(frequentIngredients{i, 2},  '.', 'Color', c(colorIndex(i),:));
        else
            plot(frequentIngredients{i, 2},  '.', 'Color', c(colorIndex(i),:));
        end
        hold on;
    end
    legend(cuisines);
    xlabel('Ingredients in top 100 edges');
    ylabel('Number of edges in which the ingredient is incident');
    title(strcat('Frequency of Ingredients in top ', num2str(numEdges), ' edges'));
    
    h1 = figure;
    h2 = figure;
    h3 = figure;
    for i=1:6
        fIngredsInEdges = frequentIngredients{i,2};
        fIngredsInEdges = (fIngredsInEdges - min(fIngredsInEdges))/(max(fIngredsInEdges) - min(fIngredsInEdges));
        fIngredsInDegree = frequentIngredients{i,4};
        fIngredsInDegree = (fIngredsInDegree - min(fIngredsInDegree))/(max(fIngredsInDegree) - min(fIngredsInDegree));
        if strcmp(mode, 'log')
            figure(h1);
            loglog(fIngredsInEdges, '.', 'Color', c(colorIndex(i), :));
            hold on;
            figure(h2);
            loglog(fIngredsInDegree, '.', 'Color', c(colorIndex(i), :));
            hold on;
            figure(h3);
            loglog(fIngredsInEdges, fIngredsInDegree, 'Color', c(colorIndex(i), :));
            hold on;
        else
            figure(h1);
            plot(fIngredsInEdges, '.', 'Color', c(colorIndex(i), :));
            hold on;
            figure(h2);
            plot(fIngredsInDegree, '.', 'Color', c(colorIndex(i), :));
            hold on;
            figure(h3);
            plot(fIngredsInEdges,fIngredsInDegree, 'Color', c(colorIndex(i), :));
            hold on;
        end
    end
    figure(h1);
    legend(cuisines);
    xlabel('Ingredients');
    ylabel('relative frequency (no. of edges in which ingredient occurs)');
    title('Ingredient frequency in top 100 edges');
    
    figure(h2);
    legend(cuisines);
    xlabel('Ingredients');
    ylabel('relative degree (wrt max frequent ingredients)');
    title('Degree distribution of ingredients');
    
    figure(h3);
    legend(cuisines);
    xlabel('Number of edges in which ingredients in top 100 edges are incident on');
    ylabel('Degree of top x frequent ingredients'); 
end