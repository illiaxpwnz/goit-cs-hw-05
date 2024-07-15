import os
import asyncio
import aiofiles
import shutil
import argparse
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

async def read_folder(source_folder, output_folder):
    tasks = []
    for root, _, files in os.walk(source_folder):
        for file in files:
            file_path = os.path.join(root, file)
            tasks.append(copy_file(file_path, output_folder))
    await asyncio.gather(*tasks)

async def copy_file(file_path, output_folder):
    file_extension = os.path.splitext(file_path)[1][1:]
    target_folder = os.path.join(output_folder, file_extension)

    if not os.path.exists(target_folder):
        os.makedirs(target_folder)
    
    target_path = os.path.join(target_folder, os.path.basename(file_path))

    try:
        async with aiofiles.open(file_path, 'rb') as src_file:
            async with aiofiles.open(target_path, 'wb') as dst_file:
                while True:
                    chunk = await src_file.read(1024)
                    if not chunk:
                        break
                    await dst_file.write(chunk)
        logging.info(f"Copied: {file_path} to {target_path}")
    except Exception as e:
        logging.error(f"Failed to copy {file_path} to {target_path}: {e}")

def main():
    parser = argparse.ArgumentParser(description='Async file sorter by extension')
    parser.add_argument('source_folder', type=str, help='Path to the source folder')
    parser.add_argument('output_folder', type=str, help='Path to the output folder')
    args = parser.parse_args()

    source_folder = args.source_folder
    output_folder = args.output_folder

    asyncio.run(read_folder(source_folder, output_folder))

if __name__ == '__main__':
    main()
