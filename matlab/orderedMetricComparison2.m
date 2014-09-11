function orderedMetricComparison2(netType, mode, metric)
    cuisines = {'indian', 'chinese', 'mexican', 'spanish', 'italian', 'french'};
    metricIndexA = -1;
    if ~isempty(metric) 
        metricIndexA = getIndex(metric);
    end
    
    h = figure;
    colorIndex = [1, 8, 25, 40, 56, 64]; 
    c = colormap(jet);
    
    for k =1:6
        subplot(3,2,k);
        [x,y] = getComparisonData(cuisines{k}, netType, metricIndexA);
        for i=1:6
            if strcmpi(mode, 'normal')
                plot(x,y{i},'.', 'color',  c(colorIndex(i),:));
                hold on;
            else
                loglog(x,y{i},'.', 'color',  c(colorIndex(i),:));
                hold on;
            end
        end
        xlabel(cuisines{k});
    end
end
     
function metricIndex = getIndex(metric)
    if strcmp(metric, 'degree')
        metricIndex = 1;
    elseif strcmp(metric, 'closeness')
        metricIndex = 2;
    elseif strcmp(metric, 'betweeness')
        metricIndex = 3;
    elseif strcmp(metric, 'eigen')
        metricIndex = 4;
    elseif strcmp(metric, 'avgNeigDegree')
        metricIndex = 5;
    elseif strcmp(metric, 'clusCoeff')
        metricIndex = 6;
    elseif strcmp(metric, 'comm')
        metricIndex = 7;
    end
end
function [x,comparisonData]=getComparisonData(cuisine, netType, i, j)
    fileName = strcat(cuisine, '_', netType, '.mat');
    [x, node] = getData(i, fileName);
    [x, orderedIndices] = sort(x, 'descend');
    comparisonData = cell(1,6);
    k=1;
    for j=1:7
        if j~=i
            [y, node] = getData(j, fileName);
            y = y(orderedIndices);
            comparisonData{k} = y;
            k = k+1;
        end
    end
end
function [x, node]=getData(i, fileName)
    load(fileName);
    switch(i)
        case 1
            x=degree;
        case 2
            x=closeness;
        case 3
            x=betCentrality;
        case 4
            x=eigenvectorCentrality;
        case 5
            x=avgNeigDegree;
        case 6
            x=clusCoeff;
        case 7
            x=communicability;
    end
end
function [xtitle, ytitle, plotTitle] = getTitle(i,j)
    xtitle = getTitleStr(i);
    ytitle = getTitleStr(j);
    plotTitle = strcat(ytitle , '-' , xtitle);
end
function title = getTitleStr(i)
    switch(i)
        case 1
            title = 'degree';
        case 2
            title = 'closeness';
        case 3
            title = 'betweeness';
        case 4
            title = 'eigen vector centrality';
        case 5
            title = 'avg Neig Degree';
        case 6
            title = 'clus coeff';
        case 7
            title = 'communicability';
    end
end