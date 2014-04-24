
function degreeRF(cuisine, metric)
     coocFile = strcat(cuisine , '_cooc.mat');
     cpFile = strcat(cuisine , '_cp.mat');
     pmiFile = strcat(cuisine , '_pmi.mat');
     ccfposFile = strcat(cuisine , '_ccf_pos.mat');
     ccfnegFile = strcat(cuisine , '_ccf_neg.mat');
     
     h = figure('Color', [0.8, 0.8, 0.8]); 
     
     plotDegreeRF(coocFile, metric, [255,255,178]);
     plotDegreeRF(cpFile, metric, [254, 204, 92]);
     plotDegreeRF(pmiFile, metric, [253,141,60]);
     plotDegreeRF(ccfposFile, metric, [240, 59, 32]);
     plotDegreeRF(ccfnegFile, metric, [189, 0, 38]);
     
     hl = legend('Cooc', 'CP', 'PMI', '+CCF', '-CCF');
     set(hl, 'color', [0.8, 0.8, 0.8]);
     title(strcat(cuisine, '-', metric, '-Rank Frequency Plot'));
     xlabel('Rank');
     ylabel('Frequency');
     set(gca,'Color',[0.8 0.8 0.8]);
     savefig(h, strcat(cuisine, '-', metric, '-RF'));
end
function plotDegreeRF(matFile, metric, rgbVal)
     rgbVal = rgbVal./255;
     [data, mulFactor] = getMetrics(matFile, metric);
     numNodesWithDeg = zeros(ceil(max(abs(data))*mulFactor)+1, 1);
     for i = 1:numel(data)
         deg = ceil(abs(data(i,1))*mulFactor);
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
     loglog(rank, numDegreesWithRank, 'Color', rgbVal);
     %hist(numNodesWithDeg, rank);
     hold on;
end
function [data, mulFactor] = getMetrics(matFile, metric)
    load(matFile);
    if strcmpi(metric, 'degree') == 1
        data=degree;
        mulFactor = 1;
    elseif strcmpi(metric, 'betweeness') == 1
        data=betCentrality;
        mulFactor = 10;
    elseif strcmpi(metric, 'closeness') == 1
        data=closeness;
        mulFactor = 100;
    elseif strcmpi(metric, 'eigen') == 1
        data=eigenvectorCentrality;
        mulFactor = 10;
    elseif strcmpi(metric, 'avgNDegree') == 1
        data=avgNeigDegree;
        mulFactor = 1;
    elseif strcmpi(metric, 'clusCoeff') == 1
        data=clusCoeff;
        mulFactor =100;
    end
end

