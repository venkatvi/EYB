function allData = plotEdgeDist(netType)
    allData=struct();
    allData = loadData('indian', netType, allData);
    allData = loadData('italian', netType, allData);
    allData = loadData('spanish', netType, allData);
    allData = loadData('mexican', netType, allData);
    allData = loadData('chinese', netType, allData);
    allData = loadData('french', netType, allData);
    
    %plotData(allData);
    %plotRF(allData);
    plotHist(allData, 0.1);
end
function plotHist(allData, threshold)
    figure;
    subplot(3,2,1);
    ind = find(allData.indian.wt > threshold);
    data = allData.indian.wt(ind);
    hist(data);
    hold on;
    subplot(3,2,2);
    ind = find(allData.italian.wt > threshold);
    data = allData.italian.wt(ind);
    hist(data);
    subplot(3,2,3);
    ind = find(allData.spanish.wt > threshold);
    data = allData.spanish.wt(ind);
    hist(data);
    subplot(3,2,4);
    ind = find(allData.mexican.wt > threshold);
    data = allData.mexican.wt(ind);
    hist(data);
    subplot(3,2,5);
    ind = find(allData.chinese.wt > threshold);
    data = allData.chinese.wt(ind);
    hist(data);
    subplot(3,2,6);
    ind = find(allData.french.wt > threshold);
    data = allData.french.wt(ind);
    hist(data);
    
    
end
function allData  = loadData(cuisine, netType, allData)
    fileName = strcat(cuisine , '_' , netType , '_wtDist.csv');
    [src, dest, wt] =  loadFile(fileName);
    allData.(cuisine).('src') = src;
    allData.(cuisine).('dest') = dest;
    allData.(cuisine).('wt') = wt;
end
function plotData(allData)
    plot(sort(allData.indian.wt), '.');
    hold on;
    plot(sort(allData.italian.wt), 'k.');
    plot(sort(allData.spanish.wt), 'r.');
    plot(sort(allData.mexican.wt), 'g.');
    plot(sort(allData.french.wt), 'm.');
    plot(sort(allData.chinese.wt), 'c.');
end
function plotRF(allData)
    figure;
    subplot(3,2,1);
    [r, n] = histPlot(allData.indian.wt);
    loglog(r, n,'.');
    subplot(3,2,2);
    [r,n] = histPlot(allData.italian.wt);
    loglog(r,n, 'k.');
    subplot(3,2,3);
    [r,n] = histPlot(allData.spanish.wt);
    loglog(r,n, 'r.');
    subplot(3,2,4);
    [r,n]=histPlot(allData.mexican.wt);
    loglog(r,n, 'g.');
    subplot(3,2,5);
    [r,n] = histPlot(allData.french.wt);
    loglog(r,n, 'm.');
    subplot(3,2,6);
    [r,n] = histPlot(allData.chinese.wt);
    loglog(r,n, 'c.');
end
function [rank, numDegreesWithRank] = histPlot(data)
    numNodesWithDeg = zeros(ceil(max(abs(data)*10000))+1, 1);
    for i = 1:numel(data)
        deg = ceil(abs(data(i,1))*10000);
        numNodesWithDeg(deg+1) = numNodesWithDeg(deg+1) + 1;
    end
    rank = sort(unique(numNodesWithDeg), 'descend');
    numDegreesWithRank = zeros(numel(rank),1);
    for i=1:numel(numNodesWithDeg)
         deg = i;
         freq = numNodesWithDeg(i);
         rankId = find(rank == freq);
         numDegreesWithRank(rankId) = numDegreesWithRank(rankId)+1;
    end
    
end