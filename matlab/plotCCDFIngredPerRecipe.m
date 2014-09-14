function plotCCDFIngredPerRecipe(fileName)
    load(fileName);
    cuisines = {'indian', 'chinese', 'mexican', 'spanish', 'french', 'italian'};
    allData = cell(numel(cuisines, 1));
    
    maxIngredients=0;
    for i=1:numel(cuisines)
        eval(sprintf('x=ingredsPerRecipe.(cuisines{%d});', i));
        allData{i} = x;
        maxIngredients = max(maxIngredients, max(x));
    end
    histbins = zeros(6, maxIngredients);
    for i=1:numel(allData)
        x = allData{i};
        for j=1:numel(x)
            ingredsPerRecipe = x(j);
            if ingredsPerRecipe > 0
                histbins(i, ingredsPerRecipe) = histbins(i, ingredsPerRecipe) + 1;
            end
        end
    end
    for i=1:6
        histbins(i,:) = histbins(i,:)/numel(allData{i});
    end
    cdf = zeros(6, size(histbins,2));
    for j=1:6
        for i=1:size(histbins,2)
            cdf(j,i) = sum(histbins(j,1:i));
        end
    end
    ccdf = 1-cdf;
    
    figure;
    bar(ccdf');
    title('CCDF of Ingredients Per Recipe');
    legend(cuisines);
    xlabel('Number of ingredients per recipe');
    ylabel('Number of recipes');
    
    figure;
    for i=1:6
        subplot(3,2,i)
        bar(ccdf(i,:))
        xlabel(strcat(cuisines{i}, '- Number of ingredients per recipe'));
        ylabel('Number of recipes');
    end
    title('CCDF of Ingredients Per Recipe');
    
%     figure;
%     colormap hot;
%     imagesc(ccdf);
%     title('CCDF of Ingredients Per Recipes');
%     set(gca,'YTickLabel',cuisines)
%     
    colorIndex = [1, 8, 25, 40, 56, 64]; 
    c = colormap(jet);
    
    figure;
    for i=1:6
        loglog(ccdf(i,:),  'Color', c(colorIndex(i),:));
        hold on;
    end
    legend(cuisines);
    title('CCDF of Ingredients Per Recipe');
    xlabel('Ingredients Per Recipe');
    ylabel('No. of Recipes');
end