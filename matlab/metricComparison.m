function metricComparison(netType, mode, metric1, metric2)
    cuisines = {'indian', 'chinese', 'mexican', 'spanish', 'italian', 'french'};
    colorIndex = [1, 8, 25, 40, 56, 64]; 
    metricIndexA = -1;
    metricIndexB = -1;
    if ~isempty(metric1) && ~isempty(metric2)
        metricIndexA = getIndex(metric1);
        metricIndexB = getIndex(metric2);
    end
    for i=1:7 %degree, betweeness, closeness, eigenvector, avgNeigDegree, clusCoeff, comm
        for j=1:7
            if i~=j && i==metricIndexA && j==metricIndexB
                h = figure;
                [xtitle, ytitle, plotTitle] = getTitle(i,j);
                plotTitle = strcat(plotTitle, '-', mode);
                c = colormap(jet);
                for k =1:6
                    subplot(3,2,k);
                    [x,y] = getComparisonData(cuisines{k}, netType, i, j);
                    if strcmpi(mode, 'normal')
                        plot(x,y,'.', 'color',  c(colorIndex(k),:));
                    else
                        loglog(x,y,'.', 'color',  c(colorIndex(k),:));
                    end
                    xlabel(cuisines{k});
                end
                annotation('textbox', [0 0.9 1 0.1], ...
                    'String', plotTitle, ...
                    'EdgeColor', 'none', ...
                    'HorizontalAlignment', 'center');
                print(h, strcat(plotTitle, '.png'));
                
                h = figure;
                for k=1:6
                    [x,y] = getComparisonData(cuisines{k}, netType, i, j);
                    if strcmpi(mode, 'log')
                        loglog(x,y,'.', 'color',  c(colorIndex(k),:));
                    else
                        plot(x,y,'.', 'color',  c(colorIndex(k),:));
                    end
                    hold on;
                end
                title(plotTitle);
                xlabel(xtitle);
                ylabel(ytitle);
                legend(cuisines);
                print(h, strcat(plotTitle, '.png'));
            end
        end
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
function [x,y]=getComparisonData(cuisine, netType, i, j)
    fileName = strcat(cuisine, '_', netType, '.mat');
    [x, node] = getData(i, fileName);
    [y, node] = getData(j, fileName);
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