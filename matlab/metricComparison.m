function metricComparison(net)
    for i=1:6 %degree, betweeness, closeness, eigenvector, avgNeigDegree, clusCoeff, comm
        for j=1:6
            if i~=j
                h = figure;
                plotTitle = getTitle(i,j);
                
                subplot(3,2,1);
                fileName = strcat('indian_', net, '.mat');
                [x,y] = getComparisonData(fileName, i, j);
                plot(x,y,'.');
                xlabel('indian');
                hold on;
                subplot(3,2,2);
                fileName = strcat('italian_', net, '.mat');
                [x,y] = getComparisonData(fileName, i, j);
                plot(x,y,'k.');
                xlabel('italian');
                subplot(3,2,3);
                fileName = strcat('spanish_', net, '.mat');
                [x,y] = getComparisonData(fileName, i, j);
                plot(x,y,'r.');
                xlabel('spanish');
                subplot(3,2,4);
                fileName = strcat('mexican_', net, '.mat');
                [x,y] = getComparisonData(fileName, i, j);
                plot(x,y,'g.');
                xlabel('mexican');
                subplot(3,2,5);
                fileName = strcat('chinese_', net, '.mat');
                [x,y] = getComparisonData(fileName, i, j);
                plot(x,y,'m.');
                xlabel('chinese');
                subplot(3,2,6);
                fileName = strcat('french_', net, '.mat');
                [x,y] = getComparisonData(fileName, i, j);
                plot(x,y,'c.');
                xlabel('french');
                annotation('textbox', [0 0.9 1 0.1], ...
                    'String', plotTitle, ...
                    'EdgeColor', 'none', ...
                    'HorizontalAlignment', 'center');
                savefig(h, strcat(plotTitle, '.fig'));
            end
        end
    end
end
function [x,y]=getComparisonData(fileName, i, j)
    x = getData(i, fileName);
    y = getData(j, fileName);
end
function x=getData(i, fileName)
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