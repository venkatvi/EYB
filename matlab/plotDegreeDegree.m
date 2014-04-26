function plotDegreeDegree(netType)
    h = figure;
    plotTitle = 'Degree-DegreePlot';
    subplot(3,2,1);
    data = getCuisineData('indian', netType);
    plot(data(:,1),data(:,2), '.');
    xlabel('indian');
    hold on;
    subplot(3,2,2);
    data = getCuisineData('italian', netType);
    plot(data(:,1),data(:,2), 'k.');
    xlabel('italian');
    subplot(3,2,3);
    data = getCuisineData('spanish', netType);
    plot(data(:,1),data(:,2),'r.');
    xlabel('spanish');
    subplot(3,2,4);
    data = getCuisineData('mexican', netType);
    plot(data(:,1),data(:,2),'g.');
    xlabel('mexican');
    subplot(3,2,5);
    data = getCuisineData('chinese', netType);
    plot(data(:,1),data(:,2),'m.');
    xlabel('chinese');
    subplot(3,2,6);
    data = getCuisineData('french', netType);
    plot(data(:,1),data(:,2), 'c.');
    xlabel('french');
    annotation('textbox', [0 0.9 1 0.1], ...
                    'String', plotTitle, ...
                    'EdgeColor', 'none', ...
                    'HorizontalAlignment', 'center');
    print(h, strcat(plotTitle, '.png'));
    
end
function data = getCuisineData(cuisine, netType)
    edgWtFile = strcat(cuisine , '_' , netType , '_wtDist.csv');
    nodeMetricsFile = strcat(cuisine, '_', netType, '_nodeMetrics.csv');
    [src, dest, wt] =  loadFile(edgWtFile);
    [node, degree] = loadFile(nodeMetricsFile);
    
    data = [];
    for i=1:numel(wt)
        s = src(i);
        ind = find(ismember(node, s) ==1);
        sdegree = str2double(degree(ind));
        
        d = dest(i);
        ind = find(ismember(node, d)==1);
        ddegree = str2double(degree(ind));
        
        k = [sdegree, ddegree, wt(i)];
        data = [data; k];
        
    end
end