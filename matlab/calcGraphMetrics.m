%% CalcGraphMetrics
% loads data from graphMetricsData.mat
% data has following columns
% cuisineId, assortativity, transitivity, avgClusteringCoefficient, degree,
% betweenesss, closeness.

% clear all
%clear all; close all;

% load graphMetrics data
load('graphMetricsData.mat');

%M = sortrows(M, 1);

startIndex = 0;
%colormap('Lines');
figure(1)
for i=1:5
    K = M(startIndex + 1:startIndex + 6, 1:8);
    K
    data = K(:,2:7)';
    plotId = M(startIndex+1, 8)*5;
    cuisineIds = K(:,1);
    subplot(6,1,plotId);
    h = bar(data);
    hold on;
    
    legend(cuisines(cuisineIds));
    title(netType(1,i));
    set(gca, 'XTickLabel', metricsType); 
    startIndex = startIndex + 6;
    
end
startIndex


