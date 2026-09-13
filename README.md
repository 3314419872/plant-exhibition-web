# 植物馆展览系统

这是一个基于 FastAPI + Vue 3 的动态网页项目，包含植物资料展示、搜索与图片识别功能。

系统设计方案见 [DESIGN.md](./DESIGN.md)。

## 启动方式

```bash
cd plant-exhibition-web
pip install -r requirements.txt
cd backend
python seed.py
uvicorn main:app --reload
```

启动后访问：`http://127.0.0.1:8000`

## 当前功能

- 植物列表展示
- 植物名称、学名、简介搜索
- 植物详情查看
- 基于图片颜色特征的简单图片检索
- SQLite 数据库

## 说明

当前图片识别使用的是颜色直方图特征，便于快速演示。后续可以替换为 ResNet50、CLIP 或其他植物识别模型，以提高准确率。

## 云端部署（Render）

1. 把本项目上传到 GitHub。
2. 在 [Render](https://render.com) 创建 Web Service。
3. 连接你的 GitHub 仓库。
4. Build Command 填写：

   ```bash
   pip install -r requirements.txt
   ```

5. Start Command 填写：

   ```bash
   cd backend && python -m uvicorn main:app --host 0.0.0.0 --port $PORT
   ```

6. 点击 Create Web Service，部署完成后 Render 会给你一个公网网址。
