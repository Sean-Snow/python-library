import requests
import os


def download(url, save_directory):
    """
    根据给定的URL下载内容，并保存到指定的目录。

    参数:
    url (str): 要下载内容的URL地址。
    save_directory (str): 保存下载内容的本地目录路径，确保目录已存在且有写入权限。
    """
    if url is None:
        return
    if not os.path.exists(save_directory):
        os.makedirs(save_directory)
    file_name = url.split('/')[-1]
    if file_name == "":
        file_name = "downloaded_file"
    save_path = os.path.join(save_directory, file_name)
    if os.path.exists(save_path):
        print(f"url 已经下载: {url}")
        return

    try:
        response = requests.get(url, stream=True)
        if response.status_code == 200:
            # 尝试从URL中获取文件名，如果无法获取则使用默认文件名
            with open(save_path, 'wb') as file:
                for chunk in response.iter_content(chunk_size=1024 * 1024):
                    if chunk:
                        file.write(chunk)
            print(f"内容已成功下载并保存到 {save_path}")
        else:
            print(f"下载失败，状态码: {response.status_code}")
    except requests.RequestException as e:
        print(f"下载出现异常: {url} {save_directory} err: {e}")
