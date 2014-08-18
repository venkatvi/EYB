function plotRFDegree(netType, mode, lt, ht, isNormalizedToNodeCount, isNormalizedToMaxDegree)
    titleStr = '';
    if isNormalizedToNodeCount
        titleStr = strcat(titleStr, '-norm by nodeCount');
    end
    if isNormalizedToMaxDegree
        titleStr = strcat(titleStr, '-norm by max degree');
    end
    cuisines = {'spanish', 'mexican', 'indian', 'chinese', 'italian', 'french'};
    h = figure;
    plotTitle = strcat('Degree RF Plot-', mode, titleStr);
    for i=1:numel(cuisines)
        subplot(3,2,i);
        sortedDegree = plotDegreeRF(cuisines{i}, netType, isNormalizedToNodeCount, isNormalizedToMaxDegree);
        if strcmpi(mode, 'log')
            loglog(sortedDegree, '.');
        else
            plot(sortedDegree, '.');
        end
        xlabel(cuisines{i});
        hold on;
    end
    annotation('textbox', [0 0.9 1 0.1], ...
                    'String', plotTitle, ...
                    'EdgeColor', 'none', ...
                    'HorizontalAlignment', 'center');
    saveas(h, plotTitle, 'png');
    
    colorIndex = [1, 8, 25, 40, 56, 64]; 
    c = colormap(jet);
    h = figure;
    
        
    plotTitle = strcat('Degree RF Plot-', mode, '-all cuisines', titleStr);
    for i=1:numel(cuisines)
        
        sortedDegree = plotDegreeRF(cuisines{i}, netType, isNormalizedToNodeCount, isNormalizedToMaxDegree);
        plt = 1;
        pht = numel(sortedDegree);
        if lt ~= -1
            plt = lt;
        end
        if ht ~= -1
            pht = ht;
        end
        if strcmpi(mode, 'log')
            loglog(sortedDegree(plt:pht), '.', 'color', c(colorIndex(i),:));
        else
            plot(sortedDegree(plt:pht), '.', 'color', c(colorIndex(i),:));
        end
        hold on;
        
    end
    legend(cuisines);
    title(plotTitle);
    saveas(h, plotTitle, 'png');
end
function sortedDegree = plotDegreeRF(cuisine, netType, isNormalizedToNodeCount, isNormalizedToMaxDegree)
     nodeMetricsFile = strcat(cuisine, '_', netType , '_nodeOrder.csv');
     [node, degree] = loadFile(nodeMetricsFile);
        
     dDegree = zeros(numel(degree),1);
     for i=1:numel(degree)
        dDegree(i) = str2double(degree{i});
     end
     
     if(isNormalizedToNodeCount)
         dDegree = dDegree / numel(node);
     end
     if(isNormalizedToMaxDegree)
         dDegree = dDegree / max(dDegree);
     end
     
     sortedDegree = sort(dDegree, 'descend');
end