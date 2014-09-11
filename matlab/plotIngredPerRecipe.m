function plotIngredPerRecipe(fileName)
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
    figure;
    bar(histbins', 'stacked');
    title('Number of recipes with binned ingredient count in a cuisine - normalized by total number of recipes in a cuisine');
    legend(cuisines);
    xlabel('Number of ingredients per recipe');
    ylabel('Number of recipes');
    
    figure;
    for i=1:6
        subplot(3,2,i)
        bar(histbins(i,:))
        xlabel(strcat(cuisines{i}, '- Number of ingredients per recipe'));
        ylabel('Number of recipes');
    end
    title('Cuisine wise - No. of  recipes with binned ingred count');
    
    figure;
    colormap hot;
    imagesc(histbins);
    title('Freq of recipes with a given ingredient count');
    set(gca,'YTickLabel',cuisines)
    
%     for i=1:6
%         histbins(i,:) = histbins(i,:)/max(histbins(i,:));
%     end
%     
%     figure;
%     title('Hist - #recipes with given ingred count - normalized by total # recipes, max ingredCount of a given cuisine');
%     bar(histbins', 'stacked');
%     legend(cuisines);
%     
%     figure;
%     title('Hist - #recipes with given ingred count - normalized by total # recipes, max ingredCount of a given cuisine');
%     for i=1:6
%         subplot(3,2,i)
%         bar(histbins(i,:))
%         xlabel(cuisines{i});
%     end
%     
%      
%     figure;
%     colormap hot;
%     imagesc(histbins);
%     title('Freq of recipes with a given ingredient count - normalized by max ingred count per recipe per cuisine');
    
end