function linkAnalysis(threshold)
    cuisines = {'indian', 'chinese', 'mexican', 'spanish', 'italian', 'french'};
    edgeWts = zeros(threshold*6, 1);
    srcs = cell(threshold*6, 1);
    dests = cell(threshold*6, 1);
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
    end
    allData = {srcs dests edgeWts};
    ingredContainer = containers.Map(char('a'), int32(0));
    for i=1:numel(srcs)
        if ingredContainer.isKey(srcs{i})
            count = ingredContainer(srcs{i});
            ingredContainer(srcs{i}) = count + 1;
        else
            ingredContainer(srcs{i}) = 1;
        end
    end
    for i=1:numel(dests)
        if ingredContainer.isKey(dests{i})
            count = ingredContainer(dests{i});
            ingredContainer(dests{i}) = count + 1;
        else
            ingredContainer(dests{i}) = 1;
        end
    end
    ingreds = ingredContainer.keys;
    ingredFreq = zeros(numel(ingreds));
    for i=1:numel(ingreds)
        count = ingredContainer(ingreds{i});
        ingredFreq(i) = count;
    end
    [ingredFreq, orderedIndices] = sort(ingredFreq, 'descend');
    sortedIngreds = ingreds(orderedIndices);
    disp a;
end