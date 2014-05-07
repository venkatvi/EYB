function plotDegreeDegree(netType, threshold )
    h = figure;
    plotTitle = strcat('Degree-DegreePlot-', num2str(threshold));
    subplot(3,2,1);
    data = getCuisineData('indian', netType, threshold );
    matrix = createMatrix(data);
    if numel(data) > 1
        plot(data(:,1),data(:,2), '.');
    end
    xlabel('indian');
    hold on;
    subplot(3,2,2);
    data = getCuisineData('italian', netType, threshold );
    if numel(data) > 1
        plot(data(:,1),data(:,2), 'k.');
    end
    xlabel('italian');
    subplot(3,2,3);
    data = getCuisineData('spanish', netType, threshold );
    if numel(data) > 1
        plot(data(:,1),data(:,2), 'r.');
    end
    xlabel('spanish');
    subplot(3,2,4);
    data = getCuisineData('mexican', netType, threshold );
    if numel(data) > 1
        plot(data(:,1),data(:,2), 'g.');
    end
    xlabel('mexican');
    subplot(3,2,5);
    data = getCuisineData('chinese', netType, threshold);
    if numel(data) > 1
        plot(data(:,1),data(:,2), 'm.');
    end
    xlabel('chinese');
    subplot(3,2,6);
    data = getCuisineData('french', netType, threshold);
    if numel(data) > 1
        plot(data(:,1),data(:,2), 'c.');
    end
    xlabel('french');
    annotation('textbox', [0 0.9 1 0.1], ...
                    'String', plotTitle, ...
                    'EdgeColor', 'none', ...
                    'HorizontalAlignment', 'center');
   % print(h, '-dpng', strcat(plotTitle, '.png'));
   % close(h);
    
end
function data = getCuisineData(cuisine, netType, threshold)
    edgWtFile = strcat(cuisine , '_' , netType , '_wtDist.csv');
    nodeMetricsFile = strcat(cuisine, '_', netType, '_nodeMetrics.csv');
    [src, dest, wt] =  loadFile(edgWtFile);
    [node, degree] = loadFile(nodeMetricsFile);
    
    oldDeg = zeros(numel(degree),1);
    for i=1:numel(degree)
        oldDeg(i) = str2double(degree{i});
    end
    
    newDeg = zeros(numel(node), 1);
    minWt = min(wt);
    maxWt = max(wt);
    
    data = [];
    for i=1:numel(wt)
        eWt = wt(i); %percent of all recipes in which this edge occurs
        s = src(i);
        sind = find(ismember(node, s) ==1);     
        
        d = dest(i);
        dind = find(ismember(node, d)==1);
        
        if sind ~= dind
            newDeg(sind) = newDeg(sind) + 1;
            newDeg(dind) = newDeg(dind) + 1;
            k = [sind, dind, eWt];
            data = [data; k];
        end
    end
    
    diff = oldDeg-newDeg;
    ind = find(diff > 0);
    if numel(ind) > 0
        j = 1;
    end
end
