function plotRFDegree(netType)
    h = figure;
    plotTitle = 'Degree RF Plot';
    subplot(3,2,1);
    [r, n] = plotDegreeRF('indian', netType);
    loglog(r,n, '.');
    xlabel('indian');
    hold on;
    subplot(3,2,2);
    [r, n] = plotDegreeRF('italian', netType);
    loglog(r,n, 'k.');
    xlabel('italian');
    subplot(3,2,3);
    [r, n] = plotDegreeRF('spanish', netType);
    loglog(r,n, 'r.');
    xlabel('spanish');
    subplot(3,2,4);
    [r, n] = plotDegreeRF('mexican', netType);
    loglog(r,n, 'g.');
    xlabel('mexican');
    subplot(3,2,5);
    [r, n] = plotDegreeRF('chinese', netType);
    loglog(r,n, 'm.');
    xlabel('chinese');
    subplot(3,2,6);
    [r, n] = plotDegreeRF('french', netType);
    loglog(r,n, 'c.');
    xlabel('french');
    annotation('textbox', [0 0.9 1 0.1], ...
                    'String', plotTitle, ...
                    'EdgeColor', 'none', ...
                    'HorizontalAlignment', 'center');
    print(h, strcat(plotTitle, '.png'));
end
function [rank, numDegreesWithRank] = plotDegreeRF(cuisine, netType)
     matFile = strcat(cuisine, '_', netType, '.mat');
     load(matFile);
     data = degree;
     nDegree = degree;
     [numDegreesWithRank, sindices] = sort(nDegree, 'descend');
     rank = 1:numel(nDegree);
     
     nodesInDecreasingDegree = node(sindices);
     f = strcat(cuisine, '_', netType , '_nodeOrder.csv');
     ff = fopen(f, 'w');
     for i=1:numel(nodesInDecreasingDegree)
         line = strcat(nodesInDecreasingDegree{i} , ',' , num2str(numDegreesWithRank(i))  );
         fprintf(ff,'%s\n',line);
     end
     fclose(ff);
%      mulFactor = 1000;
%      numNodesWithDeg = zeros(ceil(max(abs(data))*mulFactor)+1, 1);
%      for i = 1:numel(data)
%          deg = ceil(abs(data(i,1))*mulFactor);
%          numNodesWithDeg(deg+1) = numNodesWithDeg(deg+1) + 1;
%      end
%      rank = sort(unique(numNodesWithDeg), 'descend');
%      numDegreesWithRank = zeros(numel(rank),1);
%      for i=1:numel(numNodesWithDeg)
%          deg = i;
%          freq = numNodesWithDeg(i);
%          rankId = find(rank == freq);
%          numDegreesWithRank(rankId) = numDegreesWithRank(rankId)+1;
%      end
end