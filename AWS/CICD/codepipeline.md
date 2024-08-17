# Codepipeline作成

# やること
- GithubActionsにて作成したコンテナイメージがECRに格納されることを起点にCodepipelineを起動し、DBマイグレーション、ECSサービスの更新まで行う。

# 参考
- [ECS用のCDパイプラインに対する考察](https://zenn.dev/reireias/articles/8e987af2762eaa#%E8%B6%A3%E6%97%A8)
  - 様々な種類の構成のパイプラインが載っている
  - 「7. Image BuildのみGitHub Actionsでやる(複数イメージ)」がやりたいイメージ


