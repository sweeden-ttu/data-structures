namespace LangGraph;

/// <summary>Blooming-directed-graph filter agents collection (LangGraph namespace): ruby, typescript, python, csharp, java, bash, zsh, git, github, hpcc.</summary>
public static class BloomingDirectedGraphFilterAgents
{
    public static readonly IReadOnlyList<string> AgentIds = new[]
    {
        "ruby", "typescript", "python", "csharp", "java", "bash", "zsh", "git", "github", "hpcc"
    };

    public static bool IsFilterAgent(string id) => AgentIds.Contains(id);
}
