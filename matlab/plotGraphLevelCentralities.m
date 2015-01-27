function plotGraphLevelCentralities(netType)
    load graphMetrics_cooc.mat;
    
    networkdensity = edgeCount;
    for i=1:6
        networkdensity(i) = networkdensity(i)/((nodeCount(i)*(nodeCount(i)-1))/2);
    end
    data = [assortativeCoefficient, avgClusteringCoefficient, transitivity, degreeCentrality, betweeness, closeness, networkdensity];
    
    
    fileId = fopen('graphCentralities.txt', 'w');
    fprintf(fileId, '%s\n', 'Cuisine, AssortativeCoefficient, AvgClusteringCoefficient, Transitivity, Degree Centrality, Betweeneness, Closeness, Network Density');
    for i=1:6
        fprintf(fileId, '%s\n', strcat(cuisine{i}, ',', num2str(assortativeCoefficient(i)), ...
           ',', num2str(avgClusteringCoefficient(i)), ...
           ',', num2str(transitivity(i)), ...
           ',', num2str(degreeCentrality(i)),...
           ',', num2str(betweeness(i)),...
           ',', num2str(closeness(i)),...
           ',', num2str(networkdensity(i))));
    end
    fclose(fileId);
    data = data';
    figure;
    bar(data);
    title('Graph level centralities of cuisines');
    legend(cuisine');
    set(gca, 'XTickLabel', {'assortativeCoeff', 'clusCoeff', 'transitivity', 'degree', 'betweeness', 'closeness', 'networkdensity'}); 
    
    for i=1:7
        data(i,:) = abs(data(i, :))/ max(abs(data(i,:)));
    end
 
    
    figure;
    colormap(hot);
    imagesc(data);
    title('Graph level centralities of cuisines');
    set(gca, 'XTickLabel', cuisine')
    set(gca, 'YTickLabel', {'assortativeCoeff', 'clusCoeff', 'transitivity', 'degree', 'betweeness', 'closeness', 'networkdensity'});
end