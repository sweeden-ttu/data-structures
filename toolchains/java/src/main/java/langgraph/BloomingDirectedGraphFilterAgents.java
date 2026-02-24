package langgraph;

import java.util.*;

/**
 * Blooming-directed-graph filter agents collection (LangGraph namespace: graph filter agents).
 * Ten agents: ruby, typescript, python, csharp, java, bash, zsh, git, github, hpcc.
 */
public class BloomingDirectedGraphFilterAgents {
    public static final List<String> AGENT_IDS = Collections.unmodifiableList(Arrays.asList(
        "ruby", "typescript", "python", "csharp", "java", "bash", "zsh", "git", "github", "hpcc"
    ));

    public static List<String> agentIds() {
        return AGENT_IDS;
    }

    public static boolean isFilterAgent(String id) {
        return AGENT_IDS.contains(id);
    }
}
