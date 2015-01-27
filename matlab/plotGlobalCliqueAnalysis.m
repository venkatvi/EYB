function plotGlobalCliqueAnalysis(mode)
    load('globalCliqueAnalysis.mat')
    cuisines={'indian', 'chinese', 'mexican', 'spanish', 'italian', 'french'};
    colorIndex = [1, 8, 25, 40, 56, 64]; 
    c = colormap(jet);
    figure(1);
    figure(2);
    fileId1 = fopen('CliqueCount.txt', 'w');
    fprintf(fileId1, '%s\n', 'Cuisine, EdgeCount, CliqueCount');
    fileId2 = fopen('MaximalCliqueSize.txt', 'w');
    fprintf(fileId2, '%s\n', 'Cuisine, EdgeCount, MaximalCliqueSize');
    for i=1:length(cuisines)
        orderedIndices = find(strcmp(cuisine, cuisines{i}));
        edgeWtThresholds = edgeWtThreshold(orderedIndices);
        cliqueCount  = NumberOfCliques(orderedIndices);
        sizeOfMaxCliques = SizeofLargestMaximalClique(orderedIndices);
        figure(1);
        if strcmp(mode, 'log')
            loglog(edgeWtThresholds, cliqueCount, 'Color', c(colorIndex(i), :), 'Marker', '*');
        else
            plot(edgeWtThresholds, cliqueCount, 'Color', c(colorIndex(i), :), 'Marker', '*');
        end
        hold on;

        figure(2);
        if strcmp(mode, 'log')
            loglog(edgeWtThresholds, sizeOfMaxCliques, 'Color', c(colorIndex(i), :), 'Marker', '*');
        else
            plot( edgeWtThresholds, sizeOfMaxCliques, 'Color', c(colorIndex(i), :), 'Marker', '*');
        end
        hold on;
        
        for j=1:numel(edgeWtThresholds)
            fprintf(fileId1, '%s\n', strcat(cuisines{i}, ',', num2str(edgeWtThresholds(j)), ',', num2str(cliqueCount(j))));
            fprintf(fileId2, '%s\n', strcat(cuisines{i}, ',', num2str(edgeWtThresholds(j)), ',', num2str(sizeOfMaxCliques(j))));
        end
    end
    figure(1);
    legend(cuisines);
    xlabel('Edge Rank Threshold');
    ylabel('No. of cliques observed in the network pruned on edge rank threshold');
    title('No. of cliques observed vs Edge Rank Threshold');
    
    figure(2);
    legend(cuisines);
    xlabel('Edge Rank Threshold');
    ylabel('Size of maximal cliques in the network pruned on edge rank threshold');
    title('Maximal Clique Size vs Edge Rank Threshold');
    
    fclose(fileId1);
    fclose(fileId2);
end