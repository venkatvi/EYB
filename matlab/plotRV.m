function plotRV(mode, lo, hi)
    %cuisines = {'spanish', 'mexican', 'indian', 'chinese', 'italian', 'french'};
    cuisines = {'indian', 'mexican', 'french', 'italian'};
    load cuisineData
    h = figure;
    kolor = lines(10);
    top20All = {};
    top20AllNames = {};
    plotTitle = strcat(mode, '-EdgeDistributions-', num2str(lo), ':', num2str(hi));
    for i=1:numel(cuisines)
        file_name=strcat(cuisines{i}, '_edge_wts.mat');
        load(file_name);
        [sortedVal, sortedIndices] = sort(cooc/cuisineData(i,1), 'descend');
        if strcmp(mode, 'log')
            loglog(sortedVal(lo:hi),  '.', 'color', kolor(i,:));
            hold on;
        else
            plot(sortedVal(lo:hi),  '.', 'color', kolor(i,:));
            hold on;
        end
        sortedIngred1 = ingred1(sortedIndices);
        sortedIngred2 = ingred2(sortedIndices);
        ingreds = sortedIngred1(lo:hi);
        ingredstemp = sortedIngred2(lo:hi);
        for j=1:(hi-lo+1)
            ingreds{(hi-lo+1)+j} = ingredstemp{j};
        end
        top20 = unique(ingreds);
        top20All{i} = top20;
        top20AllNames{i} = cuisines{i};
    end
    legend(cuisines);
    title(plotTitle);
    print(h, '-dpng', strcat(plotTitle, '.png'));
    save(strcat('ingredientsInTop-', num2str(lo), ':', num2str(hi), '.mat'), 'top20All', 'top20AllNames');
    
end