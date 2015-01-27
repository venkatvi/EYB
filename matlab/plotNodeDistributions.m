function plotNodeDistributions(metric, net, mode, ymin, ymax)
    % plots node wise distributions of different centrality measures
    data = cell(6);
    edges = cell(6);
    binHeights = cell(6);
    cuisineNames = {'indian', 'chinese', 'mexican', 'spanish',  'italian', 'french'};
    
    
    
    [data{1}, edges{1}, binHeights{1}] = getCuisineData(metric, net, 'indian');
    [data{2}, edges{2}, binHeights{2}] = getCuisineData(metric, net, 'chinese');
    [data{3}, edges{3}, binHeights{3}] = getCuisineData(metric, net, 'mexican');
    [data{4}, edges{4}, binHeights{4}] = getCuisineData(metric, net, 'spanish');
    [data{5}, edges{5}, binHeights{5}] = getCuisineData(metric, net, 'italian');
    [data{6}, edges{6}, binHeights{6}] = getCuisineData(metric, net, 'french');
    
    fileId = fopen(['RV',' ', metric,'.txt'], 'w');
    fprintf(fileId, '%s\n', strcat('Cuisine,Rank,',metric));
    for i=1:6
        cData = data{i};
        cData = sort(cData, 'descend');
        for j=1:numel(cData)
            fprintf(fileId, '%s\n', strcat(cuisineNames{i}, ',', num2str(j), ',', num2str(cData(j))));
        end
    end
    fclose(fileId);
    
    maxVal = max(abs(data{1}));
    for i=2:6
        maxVal = max(max(abs(data{i})), maxVal);
    end
    
    figure;
    for i=1:6
        subplot(3,2, i);
        hist(data{i}, 10);
        title(cuisineNames{i});
%         tickLabels = cell(1,20);
%         for j=1:20
%             tickLabels{j} = num2str(ceil(edges{i}(j)));
%         end
        xlim([0,1]);
        ylim([0, 300]);
        %set(gca, 'XTickLabel', tickLabels);
        hold on;
    end
    
    
    combinedData = zeros(6,21);
    for i=1:6
        combinedData(i,:) = binHeights{i};
    end
    figure;
    bar(combinedData');
    xlabel('cuisines');
    legend(cuisineNames);
    title(metric);
    
    figure;
    bar(combinedData', 'stacked');
    xlabel('cuisines');
    legend(cuisineNames);
    title(metric);
    
%     h = figure;
%     colorIndex = [1, 8, 25, 40, 56, 64]; 
%     c = colormap(jet);
%     for i=1:6
%         if strcmp(mode, 'log')
%             loglog(sort(data{i}, 'descend'), '.', 'Color', c(colorIndex(i), :));
%         else
%             plot(sort(data{i}, 'descend'), '.', 'Color', c(colorIndex(i), :));
%         end
%         hold on;
%     end
%     if ~isempty(ymin) && ~isempty(ymax)
%         ylim([ymin, ymax]);
%         fileName = strcat(metric, '_cooc_rv_',mode,'_[',num2str(ymin),',', num2str(ymax),']');
%     else
%         fileName = strcat(metric, '_cooc_rv_',mode);
%     end
%     title(strcat('Node distributions of ', metric, ' for all cuisines-',mode));
%     legend(cuisineNames);
%     
%     saveas(h, fileName, 'png');
%     
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
        data = degreeCentrality;
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
%     if isBetweeness || isComm
%         ind = (data~=0);
%         data = log10(data(ind));
%     end
    
    %data = (data-min(data))/(max(data)-min(data));
    %a = min(data);
    %b = max(data);
    a = 0;
    b = 1;
    k = b-a;
    
    edges = zeros(1,20);
    j = 1;
    for i = a:k/20:b
        edges(j)  = i;
        j = j + 1;
    end
    binHeights = histc(data, edges);
end
