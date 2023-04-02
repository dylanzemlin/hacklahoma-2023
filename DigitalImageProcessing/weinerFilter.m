% Braden White %
% Hacklahoma 2023 %

close all;
clear;
clc;

originalPhoto = imread('\Users\brade\Desktop\bradenblurry.jpg');
imshow(originalPhoto);
title('Original Image');

sharpened = imsharpen(originalPhoto);
len = 20;
theta = 10;
psf = fspecial('motion', len, theta);
wiener = deconvwnr(sharpened, psf, 0);

% bw = im2gray(originalPhoto);
% wiener = deconvwnr(bw,[5 5]);

figure
imshow(wiener)
title('Test Image');