%% CalcGraphMetrics
% loads data from graphMetricsData.mat
% data has following columns
% cuisineId, assortativity, transitivity, avgClusteringCoefficient, degree,
% betweenesss, closeness.

% clear all
clear all; close all;

% load graphMetrics data
load('graphMetricsData.mat');

% normalize matrix
for i = 2:size(M, 2)-1
    col = M(:, i);
    col = col/ max(abs(col));
    M(:,i) = col;
end

M = sortrows(M, 1);

startIndex = 0;
colormap('Lines');
figure(1)
for i=1:6
    K = M(startIndex + 1:startIndex + 5, 1:8);
    K
    netTypeWiseData = K(:,2:7)';
    netTypeIds = K(:,8)*5';
    subplot(6,1,i);
    h = bar(netTypeWiseData);
    hold on;
    
    legend(netType(netTypeIds));
    title(cuisines(1,i));
    set(gca, 'XTickLabel', metricsType); 
    startIndex = startIndex + 5;
    
end
startIndex


