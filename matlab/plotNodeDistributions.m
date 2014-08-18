function plotNodeDistributions(metric, net)
    data = cell(6);
    edges = cell(6);
    binHeights = cell(6);
    cuisineName = {'spanish', 'mexican', 'indian', 'chinese', 'italian', 'french'};
    
    
    
    [data{1}, edges{1}, binHeights{1}] = getCuisineData(metric, net, 'spanish');
    [data{2}, edges{2}, binHeights{2}] = getCuisineData(metric, net, 'mexican');
    [data{3}, edges{3}, binHeights{3}] = getCuisineData(metric, net, 'indian');
    [data{4}, edges{4}, binHeights{4}] = getCuisineData(metric, net, 'chinese');
    [data{5}, edges{5}, binHeights{5}] = getCuisineData(metric, net, 'italian');
    [data{6}, edges{6}, binHeights{6}] = getCuisineData(metric, net, 'french');
    
    
    figure;
    for i=1:6
        subplot(3,2, i);
        bar(binHeights{i});
        xlabel(metric)
        title(cuisineName{i});
        tickLabels = cell(1,20);
        for j=1:20
            tickLabels{j} = num2str(edges{i}(j));
        end
        set(gca, 'XTickLabel', tickLabels);
        hold on;
    end
    
    
    combinedData = zeros(6,21);
    for i=1:6
        combinedData(i,:) = binHeights{i};
    end
    figure;
    bar(combinedData');
    xlabel('cuisines');
    legend('spanish', 'mexican', 'indian', 'chinese', 'italian', 'french');
    title(metric);
    
    figure;
    bar(combinedData', 'stacked');
    xlabel('cuisines');
    legend('spanish', 'mexican', 'indian', 'chinese', 'italian', 'french');
    title(metric);
    
end
function [data, edges, binHeights] = getCuisineData(metric, net, cuisineStr)
    fileName = strcat(cuisineStr, '_', net, '.mat');
    load(fileName);
    data = [];
    isBetweeness = 0;
    isComm = 0;
    if (strcmpi(metric, 'closeness') == 1)
        data = closeness;
    elseif (strcmpi(metric, 'betweeness') == 1)
        isBetweeness = 1;
        data = betCentrality;
    elseif (strcmpi(metric, 'eigen') == 1)
        data = eigenvectorCentrality;
    elseif (strcmpi(metric, 'degree') == 1)
        data = degree;
    elseif (strcmpi(metric, 'avgNeigDegree') == 1)
        data = avgNeigDegree;
    elseif (strcmpi(metric, 'clusCoeff') == 1)
        data = clusCoeff;
    elseif (strcmpi(metric, 'comm') == 1)
        data = communicability;
        isComm = 1;
    end
    tDataIndices = find(degree ~= 0);
       
    data = data(tDataIndices);
    if isBetweeness || isComm
        ind = (data~=0);
        data = log10(data(ind));
    end
    
    
    a = min(data);
    b = max(data);
    k = b-a;
    
    edges = zeros(1,20);
    j = 1;
    for i = a:k/20:b
        edges(j)  = i;
        j = j + 1;
    end
    binHeights = histc(data, edges);
end
