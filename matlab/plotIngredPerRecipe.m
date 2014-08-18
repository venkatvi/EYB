function plotIngredPerRecipe(fileName)
    load(fileName);
    cuisines = {'spanish', 'mexican', 'indian', 'chinese', 'italian', 'french'};
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
    
    figure;
    for i=1:6
        subplot(3,2,i)
        bar(histbins(i,:))
        xlabel(cuisines{i});
    end
    title('Cuisine wise - # recipes with binned ingred count');
    
    figure;
    colormap hot;
    imagesc(histbins);
    title('Freq of recipes with a given ingredient count');
    
    for i=1:6
        histbins(i,:) = histbins(i,:)/max(histbins(i,:));
    end
    
    figure;
    title('Hist - #recipes with given ingred count - normalized by total # recipes, max ingredCount of a given cuisine');
    bar(histbins', 'stacked');
    legend(cuisines);
    
    figure;
    title('Hist - #recipes with given ingred count - normalized by total # recipes, max ingredCount of a given cuisine');
    for i=1:6
        subplot(3,2,i)
        bar(histbins(i,:))
        xlabel(cuisines{i});
    end
    
     
    figure;
    colormap hot;
    imagesc(histbins);
    title('Freq of recipes with a given ingredient count - normalized by max ingred count per recipe per cuisine');
    
end