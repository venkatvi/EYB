function plotGrowthOfIngredsWithLinks(mode)
    cuisines = {'indian', 'chinese', 'mexican', 'spanish', 'italian', 'french'};
    thresholds = [100, 250, 500, 1000, 2500, 5000, 10000];
    figure;
    fileId = fopen('IngredGrowthWithLinks.txt', 'w');
    fprintf(fileId, '%s\n', 'Cuisine, Edges, Nodes');
    for i=1:numel(cuisines)
        fileName = strcat(cuisines{i}, '_edgeDist_dbg.csv');
        [src, dest, wt] = loadFile(fileName);
        [orderedWt, orderedIndices] = sort(wt, 'descend');
        orderedSrc = src(orderedIndices);
        orderedDest = dest(orderedIndices);
        pThresholds = thresholds;
        if numel(wt) > pThresholds(end)
            while (pThresholds(end) + 5000 < numel(wt))
                pThresholds = [pThresholds pThresholds(end) + 5000];
            end
            pThresholds = [pThresholds numel(wt)];
        end
        
        numIngreds = zeros(1, numel(pThresholds));
        for j=1:numel(pThresholds)
            threshold = pThresholds(j);
            ingreds = [orderedSrc(1:threshold) orderedDest(1:threshold)];
            uniqueIngreds = unique(ingreds);
            numIngreds(j) = length(uniqueIngreds);
            fprintf(fileId, '%s\n', strcat(cuisines{i}, ',', num2str(threshold), ',' , num2str(numIngreds(j))));
        end
        
        colorIndex = [1, 8, 25, 40, 56, 64];
        c = colormap(jet);
        
        if strcmp(mode ,'log')
            loglog(pThresholds, numIngreds, 'Marker', '*', 'Color', c(colorIndex(i), :));
            hold on;
        else
            plot(pThresholds, numIngreds, 'Marker', '*', 'Color', c(colorIndex(i), :));
            hold on;
        end
    end
    legend(cuisines);
    xlabel('Number of edges ordered by edge weight');
    ylabel('Number of ingredients');
    fclose(fileId);
end
