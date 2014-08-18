function plotCorrcoeffVsCooc(mode, lo, hi)
    cuisines = {'spanish', 'mexican', 'indian', 'chinese', 'italian', 'french'};
    load cuisineData
    %h = figure;
    kolor = lines(10);
    %plotTitle = strcat(mode, '-CorrCoeff.vs.Cooc-', num2str(lo), ':', num2str(hi));
    for i=1:numel(cuisines)
        h=figure;
        plotTitle = strcat(mode, '-', cuisines{i}, '-CorrCoeff.vs.Cooc-', num2str(lo), ':', num2str(hi));
        
        file_name=strcat(cuisines{i}, '_corrcoeff_vs_cooc.mat');
        load(file_name);
        [sortedVal, sortedIndices] = sort(cooc_rc, 'descend');
        sortedCorrcoeff = corrcoeff(sortedIndices);
        if strcmp(mode, 'log')
            loglog(sortedVal(lo:hi),sortedCorrcoeff(lo:hi),  '.', 'color', kolor(i,:));
            hold on;
        else
            plot(sortedVal(lo:hi),sortedCorrcoeff(lo:hi),  '.', 'color', kolor(i,:));
            hold on;
        end
        
        title(plotTitle);
        print(h, '-dpng', strcat(plotTitle, '.png'));
        close(h);
    end
    %legend(cuisines);
    %title(plotTitle);
    %print(h, '-dpng', strcat(plotTitle, '.png'));
    
end