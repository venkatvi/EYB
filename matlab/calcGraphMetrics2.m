%% CalcGraphMetrics
% loads data from graphMetricsData.mat
% data has following columns
% cuisineId, assortativity, transitivity, avgClusteringCoefficient, degree,
% betweenesss, closeness.

% clear all
%clear all; close all;

% load graphMetrics data
load('graphMetrics.mat');

M = [cuisine, assortativity, transitivity, avgClustCoeff, degree, betweeness, closeness,  nettype];
startIndex = 0;

mycolor = [255,255,178;254, 204, 92;253,141,60;240, 59, 32;189, 0, 38];
mycolor = mycolor./255;
colormap(mycolor);

%colormap('Lines');
figure(1)
for i=1:5
    
    K = M(startIndex + 1:startIndex + 6, 1:8);
    K
    data = K(:,2:7)';
    plotId = M(startIndex+1, 8);
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

