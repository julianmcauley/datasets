clear all;
close all;

% Load CSV file with levensthein distances
load('hist_lev.csv');
% If output_pdf = 1, save plot in pdf format
output_pdf = 1;

% Plot histogram of Levenshtein distances
n = 10;
histogram(hist_lev(hist_lev<=n))

% Add title, legend, axis limits...
xlim([-0.5 10.5])
title('Levenshtein distance between game names');
hx = xlabel('Levenshtein distance');
hy = ylabel('Number of games');
set(gca,'fontsize',15,'fontname','Helvetica','box','off','tickdir','out','ticklength',[.01 .01],'xcolor',0.5*[1 1 1],'ycolor',0.5*[1 1 1]);
set([hx; hy],'fontsize',18,'fontname','avantgarde','color',[.3 .3 .3]);
grid on;

% Create a pdf file with histogram
if (output_pdf)
  disp('printing the figure');
  set(gcf, 'PaperUnits', 'centimeters');
  set(gcf, 'PaperPosition', [0 0 20 12]);
  set(gcf, 'PaperSize', [20 12]);
  print -dpdf 'histogram_lev.pdf'
end;
