function perCuisineLinkAnalysis(thresholds)
load IngredientsGrowthWithLinks.mat
cuisines = {'indian', 'chinese', 'mexican', 'spanish', 'italian', 'french'};
yvalues = zeros(length(thresholds),6);
for i=1:numel(thresholds)
    threshold = thresholds(i);
    perThresholdContainer = thresholdContainerPerCuisine(threshold);
    
    for i1=1:numel(cuisines)
        ingreds = perThresholdContainer(cuisines{i1});
        yvalues(i, i1) = length(ingreds);
    end
end

colorIndex = [1, 8, 25, 40, 56, 64]; 
c = colormap(jet);

figure;
for i=1:6
    plot(yvalues(:,i)', 'Marker', '*', 'Color', c(colorIndex(i), :));
    hold on;
end
legend(cuisines);
xlabel('links');
ylabel('ingredients per cuisine');
title('Growth of ingredient count in networks with links per cuisine');


figure;
for i=1:6
    loglog(yvalues(:,i)', 'Marker', '*', 'Color', c(colorIndex(i), :));
    hold on;
end
legend(cuisines);
xlabel('links');
ylabel('ingredients per cuisine');
title('loglog - Growth of ingredient count in networks with links per cuisine');

end