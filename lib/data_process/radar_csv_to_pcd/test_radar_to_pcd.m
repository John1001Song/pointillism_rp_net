data = readtable("./test_data/left/frame0.csv")

% Extract the X, Y, Z columns
xyzPoints = data{:, {'X', 'Y', 'Z'}};

% Display the first few rows of the extracted data (optional)
disp(xyzPoints(1:5, :));

% Create a point cloud object from the X, Y, Z data
ptCloud = pointCloud(xyzPoints);

% Inspect the properties of the point cloud object
disp(ptCloud);

% Display the point cloud
pcshow(ptCloud);
title('3D Point Cloud from Radar Data');
xlabel('X');
ylabel('Y');
zlabel('Z');

% Step 5: Save the point cloud to a PCD file
output_pcd_path = './output.pcd';
pcwrite(ptCloud, output_pcd_path);

disp(['Point cloud saved to ', output_pcd_path]);
