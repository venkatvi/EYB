function metricComparison(netType)
    for i=1:6 %degree, betweeness, closeness, eigenvector, avgNeigDegree, clusCoeff, comm
        for j=1:6
            if i~=j
                h = figure;
                plotTitle = getTitle(i,j);
                subplot(3,2,1);
                [x,y] = getComparisonData('indian', netType, i, j);
                plot(x,y,'.');
                xlabel('indian');
                hold on;
                subplot(3,2,2);
                [x,y] = getComparisonData('italian', netType, i, j);
                plot(x,y,'k.');
                xlabel('italian');
                subplot(3,2,3);
                [x,y] = getComparisonData('spanish', netType, i, j);
                plot(x,y,'r.');
                xlabel('spanish');
                subplot(3,2,4);
                [x,y] = getComparisonData('mexican', netType, i, j);
                plot(x,y,'g.');
                xlabel('mexican');
                subplot(3,2,5);
                [x,y] = getComparisonData('chinese', netType, i, j);
                plot(x,y,'m.');
                xlabel('chinese');
                subplot(3,2,6);
                [x,y] = getComparisonData('french', netType, i, j);
                plot(x,y,'c.');
                xlabel('french');
                annotation('textbox', [0 0.9 1 0.1], ...
                    'String', plotTitle, ...
                    'EdgeColor', 'none', ...
                    'HorizontalAlignment', 'center');
                print(h, strcat(plotTitle, '.png'));
            end
        end
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
function plotTitle = getTitle(i,j)
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