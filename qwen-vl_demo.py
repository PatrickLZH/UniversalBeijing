import os
import base64
from openai import OpenAI
from pathlib import Path

class ImageAnalyzer:
    def __init__(self, api_key=None):
        """
        初始化图像分析器
        """
        self.client = OpenAI(
            api_key=api_key or os.getenv("DASHSCOPE_API_KEY"),
            base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
        )
        self.documents_path = Path('documents').resolve()
    
    def get_image_files(self, image_type='image'):
        """
        获取指定目录下的所有图片文件路径
        
        Args:
            image_type (str): 图片文件夹名称
            
        Returns:
            list: 图片文件路径列表
        """
        image_dir = self.documents_path / image_type
        print(image_dir)
        if not image_dir.exists():
            raise FileNotFoundError(f"目录不存在: {image_dir}")
        
        image_files = []
        # 支持多种图片格式
        supported_formats = {'.png', '.jpg', '.jpeg', '.gif', '.bmp', '.webp'}
        
        for file_path in image_dir.iterdir():
            if file_path.is_file() and file_path.suffix.lower() in supported_formats:
                image_files.append(file_path)
        
        return image_files
    
    def encode_image_to_base64(self, image_path):
        """
        将图片文件编码为base64字符串
        
        Args:
            image_path (Path): 图片文件路径
            
        Returns:
            str: base64编码的图片数据
        """
        try:
            with open(image_path, "rb") as image_file:
                return base64.b64encode(image_file.read()).decode('utf-8')
        except Exception as e:
            raise Exception(f"读取图片文件失败 {image_path}: {str(e)}")
    
    def analyze_image(self, image_path, prompt="这张图描绘了什么内容？"):
        """
        分析单张图片
        
        Args:
            image_path (Path): 图片文件路径
            prompt (str): 分析提示词
            
        Returns:
            str: 分析结果
        """
        # 获取图片的base64编码
        image_base64 = self.encode_image_to_base64(image_path)
        
        # 构造图片数据URL
        image_extension = image_path.suffix.lower()
        mime_type = self._get_mime_type(image_extension)
        image_url = f"data:{mime_type};base64,{image_base64}"
        
        # 调用模型API
        try:
            completion = self.client.chat.completions.create(
                model="qwen2-vl-2b-instruct",
                messages=[
                    {
                        "role": "system", 
                        "content": [{"type": "text", "text": "You are a helpful assistant."}]
                    },
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "image_url",
                                "image_url": {"url": image_url},
                            },
                            {"type": "text", "text": prompt},
                        ],
                    }
                ],
            )
            return completion.choices[0].message.content
        except Exception as e:
            raise Exception(f"分析图片失败 {image_path}: {str(e)}")
    
    def analyze_images_batch(self, image_type='image', prompt="这张图描绘了什么内容？"):
        """
        批量分析图片
        
        Args:
            image_type (str): 图片文件夹名称
            prompt (str): 分析提示词
            
        Yields:
            tuple: (图片路径, 分析结果)
        """
        image_files = self.get_image_files(image_type)
        
        for image_path in image_files:
            try:
                result = self.analyze_image(image_path, prompt)
                yield (image_path, result)
            except Exception as e:
                yield (image_path, f"分析失败: {str(e)}")
    
    def _get_mime_type(self, extension):
        """
        根据文件扩展名获取MIME类型
        
        Args:
            extension (str): 文件扩展名
            
        Returns:
            str: MIME类型
        """
        mime_types = {
            '.png': 'image/png',
            '.jpg': 'image/jpeg',
            '.jpeg': 'image/jpeg',
            '.gif': 'image/gif',
            '.bmp': 'image/bmp',
            '.webp': 'image/webp'
        }
        return mime_types.get(extension, 'image/jpeg')

def main():
    """
    主函数 - 演示如何使用ImageAnalyzer
    """
    try:
        # 初始化分析器
        analyzer = ImageAnalyzer()
        
        # 批量分析图片
        print("开始分析图片...")
        for image_path, result in analyzer.analyze_images_batch('image'):
            print(f"\n图片: {image_path.name}")
            print(f"分析结果: {result}")
            print("-" * 50)
            
    except Exception as e:
        print(f"程序执行出错: {str(e)}")

if __name__ == "__main__":
    main()