function getMostFrequentIngredients(numEdges, mode)
    cuisines = {'indian', 'chinese', 'mexican', 'spanish', 'italian', 'french'};
    dataPerLinkThreshold = containers.Map(int32(0), ?handle);
    for j=1:length(numEdges)
        links = numEdges(j);
        frequentIngredients = cell(6,4);    
        for i=1:6
            fileName1 = strcat(cuisines{i}, '_cooc.mat');
            load(fileName1);

            [sortedDegree, sortedIndices] = sort(degree, 'descend');
            sortedNodeNames = node(sortedIndices);
            topFrequentIngredients{i, 1} = sortedNodeNames;

            fileName2 = strcat(cuisines{i}, '_edge_wts.mat');
            load(fileName2);
            [sortedCooccurrence, sortedIndices] = sort(cooc, 'descend');
            sortedIngred1 = ingred1(sortedIndices);
            sortedIngred2 = ingred2(sortedIndices);

            sortedIngreds = containers.Map(char('a'), int32(0));
            for i1=1:links
                if (sortedIngreds.isKey(sortedIngred1{i1}))
                    sortedIngreds(sortedIngred1{i1}) = sortedIngreds(sortedIngred1{i1}) + 1;
                else
                    sortedIngreds(sortedIngred1{i1}) = 1;
                end
                if (sortedIngreds.isKey(sortedIngred2{i1}))
                    sortedIngreds(sortedIngred2{i1}) = sortedIngreds(sortedIngred2{i1}) + 1;
                else
                    sortedIngreds(sortedIngred2{i1}) = 1;
                end
            end
            sortedIngreds.remove('a');
            temp = sortedIngreds.values;
            sortedIngredsFrequency = zeros(numel(temp), 1);
            for i1=1:numel(temp)
                sortedIngredsFrequency(i1) = temp{i1};
            end
            [sortedFrequencies, sortedIndices] = sort(sortedIngredsFrequency, 'descend');
            sortedIngredKeys = sortedIngreds.keys;
            sortedIngreds = sortedIngredKeys(sortedIndices);
            
            cnt = numel(sortedIngreds);
            if numel(sortedIngreds) > length(sortedDegree)
                cnt = length(sortedDegree);
            end
            topDegree = sortedDegree(1:cnt);
            topIngreds = sortedNodeNames(1:cnt);


            frequentIngredients{i,1} = sortedIngreds(1:numel(sortedIngreds)-1)';
            frequentIngredients{i,2} = sortedFrequencies(1:numel(sortedIngreds)-1);
            frequentIngredients{i,3} = topIngreds;
            frequentIngredients{i,4} = topDegree;
        end
        dataPerLinkThreshold(links) = frequentIngredients;
    end
    
    save('frequentIngreds.mat', 'dataPerLinkThreshold');
    data = dataPerLinkThreshold;
    data.remove(0);
    keys = data.keys;
    for i=1:length(keys)
        links = keys{i};
        value = data(links);
        cuisines = {'indian', 'chinese', 'mexican', 'spanish', 'italian', 'french'};
        for j=1:6
            fileName = strcat(cuisines{j}, '_', num2str(links), '.csv');
            fid = fopen(fileName, 'wt');
            topIngredsInLinks = value{j,1};
            topIngredsBydegree = value{j,3};
            alreadyHitForDest = zeros(1, length(topIngredsBydegree));
            alreadyHitForSrc = zeros(1, length(topIngredsInLinks));
            for k =1:numel(topIngredsInLinks)
                alreadyHit = 0;
                for l = 1:numel(topIngredsBydegree)
                    if strcmp(topIngredsInLinks{k}, topIngredsBydegree{l})
                        alreadyHitForSrc(k) =alreadyHitForSrc(k) + 1;
                        alreadyHitForDest(l) = alreadyHitForDest(l) + 1;
                        line = strcat(topIngredsInLinks{k}, ',', num2str(k), ',' , topIngredsBydegree{l}, ',', num2str(l), ',1\n');
                        fprintf(fid, line);
                        
                    end
                end
            end
            ind =  find(alreadyHitForDest == 0);
            if ~isempty(ind)
                for k = 1:length(ind)
                    l = ind(k);
                    line = strcat(' ,', num2str(length(topIngredsInLinks)+1), ',', topIngredsBydegree{l}, ',' , num2str(l), ',1\n');
                    fprintf(fid, line);
                end
            end
            ind = find(alreadyHitForSrc == 0);
            if ~isempty(ind)
                for k = 1:length(ind)
                    l = ind(k);
                    line = strcat(topIngredsInLinks{l}, ',', num2str(l), ', ,', num2str(length(topIngredsBydegree)+1), ',1\n');
                    fprintf(fid,line);
                end
            end
            fclose(fid);  
        end
    end
    figure;
    colorIndex = [1, 8, 25, 40, 56, 64]; 
    c = colormap(jet);
    for i=1:6
        if strcmp(mode, 'log')
            loglog(frequentIngredients{i, 2},  'Marker', '.', 'Color', c(colorIndex(i),:));
        else
            plot(frequentIngredients{i, 2},  'Marker', '.', 'Color', c(colorIndex(i),:));
        end
        hold on;
    end
    legend(cuisines);
    xlabel('Ingredients in top 100 edges');
    ylabel('Number of edges in which the ingredient is incident');
    title(strcat('Frequency of Ingredients in top ', num2str(numEdges), ' edges'));
    
%     h1 = figure;
%     h2 = figure;
%     h3 = figure;
%     for i=1:6
%         fIngredsInEdges = frequentIngredients{i,2};
%         fIngredsInEdges = (fIngredsInEdges - min(fIngredsInEdges))/(max(fIngredsInEdges) - min(fIngredsInEdges));
%         fIngredsInDegree = frequentIngredients{i,4};
%         fIngredsInDegree = (fIngredsInDegree - min(fIngredsInDegree))/(max(fIngredsInDegree) - min(fIngredsInDegree));
%         if strcmp(mode, 'log')
%             figure(h1);
%             loglog(fIngredsInEdges, 'Marker', '.', 'Color', c(colorIndex(i), :));
%             hold on;
%             figure(h2);
%             loglog(fIngredsInDegree, 'Marker', '.', 'Color', c(colorIndex(i), :));
%             hold on;
%             figure(h3);
%             loglog(fIngredsInEdges, fIngredsInDegree, 'Color', c(colorIndex(i), :));
%             hold on;
%         else
%             figure(h1);
%             plot(fIngredsInEdges, 'Marker', '.', 'Color', c(colorIndex(i), :));
%             hold on;
%             figure(h2);
%             plot(fIngredsInDegree, 'Marker', '.', 'Color', c(colorIndex(i), :));
%             hold on;
%             figure(h3);
%             plot(fIngredsInEdges,fIngredsInDegree, 'Color', c(colorIndex(i), :));
%             hold on;
%         end
%     end
%     figure(h1);
%     legend(cuisines);
%     xlabel('Ingredients');
%     ylabel('relative frequency (no. of edges in which ingredient occurs)');
%     title('Ingredient frequency in top 100 edges');
%     
%     figure(h2);
%     legend(cuisines);
%     xlabel('Ingredients');
%     ylabel('relative degree (wrt max frequent ingredients)');
%     title('Degree distribution of ingredients');
%     
%     figure(h3);
%     legend(cuisines);
%     xlabel('Number of edges in which ingredients in top 100 edges are incident on');
%     ylabel('Degree of top x frequent ingredients'); 
end