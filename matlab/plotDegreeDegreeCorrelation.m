function plotDegreeDegreeCorrelation(netType, threshold )
    cuisines = {'spanish', 'mexican', 'indian', 'chinese', 'italian', 'french'};
    colorIndex = [1, 8, 25, 40, 56, 64]; 

    for i=1:6
        h = figure;
        colormap hot;
        data = getCuisineData(cuisines{i}, netType, threshold );
        imagesc(data);
        title(strcat('Degree-Degree-Correlation-', cuisines{i}));
    end
    
end
function DegreeDegreeCorrelation = getCuisineData(cuisine, netType, threshold)
    edgWtFile = strcat(cuisine , '_' , netType , '_wtDist.csv');
    nodeMetricsFile = strcat(cuisine, '_', netType, '_nodeMetrics.csv');
    [src, dest, wt] =  loadFile(edgWtFile);
    [node, degree] = loadFile(nodeMetricsFile);
    
    dDeg = zeros(numel(degree),1);
    for i=1:numel(degree)
        dDeg(i) = str2double(degree{i});
    end
    
    
    
    maxDegree = max(dDeg);
    
    DegreeDegreeCorrelation = zeros(maxDegree, maxDegree);
    for i=1:numel(wt)
        s = src(i);
        sind = find(ismember(node, s) ==1);     
        
        d = dest(i);
        dind = find(ismember(node, d)==1);
        
        if sind ~= dind
            degreeOfX = dDeg(sind);
            degreeOfY = dDeg(dind);
            DegreeDegreeCorrelation(degreeOfX, degreeOfY) = DegreeDegreeCorrelation(degreeOfX, degreeOfY) + 1;
        end
    end
    
    
end
