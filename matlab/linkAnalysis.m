function linkAnalysis(thresholds)
    cuisines = {'indian', 'chinese', 'mexican', 'spanish', 'italian', 'french'};
    
    thresholdContainer = containers.Map(int32(0), ?handle);
    
    xvalues = zeros(numel(thresholds,1));
    yvalues = zeros(numel(thresholds,1));
    
    thresholdContainerPerCuisine = containers.Map(int32(0), ?handle);
    
    for i1 = 1:numel(thresholds)
        threshold = thresholds(i1);
        edgeWts = zeros(threshold*6, 1);
        srcs = cell(threshold*6, 1);
        dests = cell(threshold*6, 1);
        
        cuisineContainer = containers.Map(char('a'), ?handle);
        
        k = 0;
        for i=1:6
            
            edgWtFile = strcat(cuisines{i} , '_cooc_wtDist.csv');
            [src, dest, wt] =  loadFile(edgWtFile);
            [wt, orderedIndices] = sort(wt, 'descend');
            subsetIndices = orderedIndices(1:threshold);
            a = src(subsetIndices);
            b = dest(subsetIndices);
            srcs(k+1:k+threshold, 1) = a;
            dests(k+1:k+threshold, 1) = b;
            edgeWts(k+1:k+threshold, 1) = wt(1:threshold);
            k = k+threshold;
            
            cuisineWiseIngredContainer = containers.Map(char('a'), int32(0));
            addToContainer(a, cuisineWiseIngredContainer);
            addToContainer(b, cuisineWiseIngredContainer);
            cuisineContainer(cuisines{i}) = cuisineWiseIngredContainer;
                        
        end
        
        thresholdContainerPerCuisine(threshold) = cuisineContainer;
        allData = {srcs dests edgeWts};
        ingredContainer = containers.Map(char('a'), int32(0));
        addToContainer(srcs, ingredContainer);
        addToContainer(dests, ingredContainer);
        ingreds = ingredContainer.keys;
        ingredFreq = zeros(numel(ingreds, 1));
        for i=1:numel(ingreds)
            count = ingredContainer(ingreds{i});
            ingredFreq(i) = count;
        end
        [ingredFreq, orderedIndices] = sort(ingredFreq, 'descend');
        sortedIngreds = ingreds(orderedIndices);
        thresholdContainer(threshold) = {ingredFreq, sortedIngreds, allData};
        xvalues(i1) = threshold;
        yvalues(i1) = length(ingredFreq);
    end
    save('IngredientsGrowthWithLinks.mat', 'thresholdContainer', 'thresholdContainerPerCuisine');
    figure;
    plot(xvalues, yvalues, '.');
    figure;
    loglog(xvalues, yvalues, '.');
end
function addToContainer(data, container)
    for i=1:numel(data)
        if container.isKey(data{i})
            count = container(data{i});
            container(data{i}) = count + 1;
        else
            container(data{i}) = 1;
        end
    end
end