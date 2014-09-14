function perCuisineCliqueAnalysis(mode)
    cuisines = {'indian', 'chinese', 'mexican', 'spanish', 'italian', 'french'};
    thresholds = [100, 250, 500, 1000];
    
    colorIndex = [1, 8, 25, 40, 56, 64]; 
    c = colormap(jet);
    for i=1:length(thresholds)
        figure(1);
        figure(2);
        figure(3);
        figure(4);
        figure(5);
        for j=1:length(cuisines)
            fileName = strcat(cuisines{j}, '_', num2str(thresholds(i)), '_cliqueInfo.mat');
            load(fileName);
            if strcmp(mode, 'log')
                figure(1);
                loglog(Rank, Degree, 'Marker', '.', 'LineStyle', '-', 'Color', c(colorIndex(j), :));
                hold on;
                figure(2);
                loglog(Rank, NumberOfCliques, 'Marker', '.', 'Color', c(colorIndex(j), :));
                hold on;
                figure(3);
                loglog(Rank, SizeofLargestMaximalClique, 'Marker', '.', 'Color', c(colorIndex(j), :), 'LineStyle', '-.');
                hold on;
                figure(4);
                loglog(Degree, NumberOfCliques, 'Marker', '.', 'Color', c(colorIndex(j), :), 'LineStyle', '-.');
                hold on;
                figure(5);
                loglog(Degree, SizeofLargestMaximalClique, 'Marker', '.', 'Color', c(colorIndex(j), :), 'LineStyle', '-.');
                hold on;
            else
                figure(1);
                plot(Rank, Degree, 'Marker', '.', 'LineStyle', '-', 'Color', c(colorIndex(j), :));
                hold on;
                figure(2);
                plot(Rank, NumberOfCliques, 'Marker', '.', 'Color', c(colorIndex(j), :));
                hold on;
                figure(3);
                plot(Rank, SizeofLargestMaximalClique, 'Marker', '.', 'Color', c(colorIndex(j), :), 'LineStyle', '-.');
                hold on;
                figure(4);
                plot(Degree, NumberOfCliques, 'Marker', '.', 'Color', c(colorIndex(j), :), 'LineStyle', '-.');
                hold on;
                figure(5);
                plot(Degree, SizeofLargestMaximalClique, 'Marker', '.', 'Color', c(colorIndex(j), :), 'LineStyle', '-.');
                hold on;
            end
        end
        h = figure(1);
        legend(cuisines);
        xlabel(strcat('Rank of Ingredients in pruned network of top ', num2str(thresholds(i)), ' links'));
        ylabel('Degree of Ingredients');
        title('Degree vs Rank')
        fileName = strcat('Degree-vs-Rank - PrunedNetwork-', num2str(thresholds(i)), 'links-', mode);
        saveas(h, fileName, 'png');
        
        h = figure(2);
        legend(cuisines);
        xlabel(strcat('Rank of Ingredients in pruned network of top ', num2str(thresholds(i)), ' links'));
        ylabel('Number of Cliques observed for a given ingredient');
        title('Cliques vs Rank')
        fileName = strcat('CliqueCount-vs-Rank - PrunedNetwork-', num2str(thresholds(i)), 'links-', mode);
        saveas(h, fileName, 'png');
        
        h = figure(3);
        legend(cuisines);
        xlabel(strcat('Rank of Ingredients in pruned network of top ', num2str(thresholds(i)), ' links'));
        ylabel('Size of Largest Maximal Clique observed for a given ingredient');
        title('Largest Maximal Clique Size vs Rank')
        fileName = strcat('MaxCliqueSize-vs-Rank - PrunedNetwork-', num2str(thresholds(i)), 'links-',mode);
        saveas(h, fileName, 'png');
        
        h = figure(4);
        legend(cuisines);
        xlabel(strcat('Degree of Ingredients in pruned network of top ', num2str(thresholds(i)), ' links'));
        ylabel('Number of Cliques observed for a given ingredient');
        title('Cliques vs Degree')
        fileName = strcat('CliqueCount-vs-Degree - PrunedNetwork-', num2str(thresholds(i)), 'links-', mode);
        saveas(h, fileName, 'png');
        
        
        h = figure(5);
        legend(cuisines);
        xlabel(strcat('Degree of Ingredients in pruned network of top ', num2str(thresholds(i)), ' links'));
        ylabel('Size of Largest Maximal Clique observed for a given ingredient');
        title('Largest Maximal Clique Size vs Degree')
        fileName = strcat('MaxCliqueSize-vs-Degree - PrunedNetwork-', num2str(thresholds(i)), 'links-', mode);
        saveas(h, fileName, 'png');
    end
    
end