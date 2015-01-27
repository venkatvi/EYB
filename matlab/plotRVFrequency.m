function plotRVFrequency(mode)
    cuisines = {'indian', 'chinese', 'mexican', 'spanish', 'french', 'italian'};
    load ingredsPerRecipe.mat;
    h1 = figure;
    h2 = figure;
    h3 = figure;
    colorIndex = [1, 8, 25, 40, 56, 64]; 
    c = colormap(jet);
    fileId1 = fopen('RVFrequencyNormalized.txt', 'w');
    fileId2 = fopen('RVFrequency.txt', 'w');
    fileId3 = fopen('RVBucketedFrequency.txt', 'w');
    fprintf(fileId1, '%s\n', 'Cuisine,Rank,NormalizedFrequency');
    fprintf(fileId2, '%s\n', 'Cuisine,Rank,Frequency');
    fprintf(fileId3, '%s\n', 'Cuisine,Rank,BinnedFrequency');
    for i=1:6
        fileName = strcat(cuisines{i}, '_ingredFreq.csv');
        [ingredients, freq] = loadFile(fileName);
        [ingredients, freq] = removeIngredients(ingredients, freq);
        nFreq = zeros(1, numel(freq));
        for i1=1:length(freq)
            nFreq(i1) = str2num(freq{i1});
        end
        [sortedFrequencies, sortedIndices] = sort(nFreq, 'descend');
        sortedFreqIngreds = ingredients(sortedIndices);
        
        binnedFreq = zeros(1, max(sortedFrequencies));
        prevFreq = sortedFrequencies(1);
        prevRank = 1; 
        rank = zeros(1, numel(sortedFrequencies));
        rank(1) = 1;
        for j=2:numel(sortedFrequencies)
            if sortedFrequencies(j) == prevFreq
                rank(j) = prevRank;
            else
                rank(j) = prevRank + 1;
                prevRank = prevRank + 1; 
                prevFreq = sortedFrequencies(j);
            end
            
            if sortedFrequencies(j) > 0
                binnedFreq(sortedFrequencies(j)) = binnedFreq(sortedFrequencies(j)) + 1;
            end
        end
        
        eval(sprintf('x=ingredsPerRecipe.(cuisines{%d});', i));
        normalizedFrequencies = sortedFrequencies./numel(x);
        if strcmp(mode, 'log')
            figure(h1);
            loglog(rank, sortedFrequencies,  '.', 'Color', c(colorIndex(i),:));
            hold on;
            
            figure(h2);
            loglog(binnedFreq,  '.', 'Color', c(colorIndex(i),:));
            hold on;
            
            figure(h3);
            loglog(rank, normalizedFrequencies,  '.', 'Color', c(colorIndex(i),:));
            hold on;
            
        else
            figure(h1);
            plot(rank, sortedFrequencies,  '.', 'Color', c(colorIndex(i),:));
            hold on;
            figure(h2);
            plot(binnedFreq,  '.', 'Color', c(colorIndex(i),:));
            hold on;
            figure(h3);
            plot(rank, normalizedFrequencies,  '.', 'Color', c(colorIndex(i),:));
            hold on;
        end
        hold on;
        for j=1:numel(sortedFrequencies)
            fprintf(fileId1, '%s\n', strcat(cuisines{i}, ',', num2str(rank(j)), ',', num2str(normalizedFrequencies(j))));
        end
        for j=1:numel(binnedFreq)
            fprintf(fileId3, '%s\n', strcat(cuisines{i}, ',', num2str(j), ',', num2str(binnedFreq(j))));
        end
        for j=1:numel(normalizedFrequencies)
            fprintf(fileId2, '%s\n', strcat(cuisines{i}, ',', num2str(rank(j)), ',', num2str(sortedFrequencies(j))));
        end
    end
    fclose(fileId1);
    fclose(fileId2);
    fclose(fileId3);
    figure(h1);
    legend(cuisines);
    xlabel('Rank of Ingredients');
    ylabel('Number of Recipes in which the ingredient occur');
    title('Rank-Value plot of Ingredient Frequency in Recipes');
    
    figure(h2);
    legend(cuisines);
    xlabel('Frequency of Occurence'); 
    ylabel('Number of Ingredients With Frequency X');
    title('?');
    
    figure(h3);
    legend(cuisines);
    xlabel('Rank of Ingredients');
    ylabel('Number of Recipes in which the ingredient occur');
    title('Rank-Value plot of Ingredient Frequency in Recipes');
    
end
function [nodeNames, data] = removeIngredients(nodeNames, data)
    indicesToRemove = [];
    indicesToRemove = addIndexOf(nodeNames, 'stick', indicesToRemove);
    indicesToRemove = addIndexOf(nodeNames, 'ingredient', indicesToRemove);
    indicesToRemove = addIndexOf(nodeNames, 'paste', indicesToRemove);
    indicesToRemove = addIndexOf(nodeNames, 'split', indicesToRemove);
    if ~isempty(indicesToRemove)
        nodeNames(indicesToRemove) = [];
        data(indicesToRemove) = [];
    end
end
function indicesToRemove = addIndexOf(nodeNames, nodeToRemove, indicesToRemove)
    index =strmatch(nodeToRemove, nodeNames, 'exact');
    if ~isempty(index)
        indicesToRemove = [indicesToRemove;index];
    end
end