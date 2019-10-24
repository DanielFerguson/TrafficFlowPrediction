import os

for root, dirs, files in os.walk('C:/model/'):
    for filename in files:
        name = filename.split('_')[0] + '_' + filename.split('_')[1]

        # Make a directory for the fole
        os.mkdir(f'C:/models/{name}')

        # Convert the model
        os.system(
            f'tensorflowjs_converter --input_format keras C:/model/{filename} C:/models/{name}')

        print(f'Finished {name}')
