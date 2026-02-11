# ReAct
```
def react_loop(task, tools, max_iterations=5):
    """Simplified ReAct algorithm"""
    context = []

    for i in range(max_iterations):
        # 1. Reasoning step
        thought = llm.generate_thought(task, context)

        # 2. Decide on action
        action, action_input = llm.decide_action(thought, tools)

        # 3. Execute action
        if action == "FINISH":
            return generate_final_answer(context)

        observation = execute_tool(action, action_input)

        # 4. Update context
        context.append({
            "thought": thought,
            "action": action,
            "observation": observation
        })

    return generate_final_answer(context)
```

## When to Use ReAct

Ideal Use Cases

✅ Question answering with web search

Agent reasons about what to search
Executes search queries
Synthesizes results into answers
✅ API orchestration

Determines which APIs to call
Makes API requests based on responses
Adapts strategy based on results
✅ Data gathering tasks

Decides what data to collect
Uses tools to retrieve data
Continues until sufficient information gathered
✅ Interactive workflows

Reasons about next steps
Executes actions
Adjusts based on outcomes

## When NOT to Use ReAct

❌ Pure reasoning tasks → Use Self-Discovery or Reflection ❌ Predetermined workflows → Use Plan & Solve ❌ Cost-sensitive tool usage → Use REWOO ❌ Tasks requiring learning from failures → Use Reflexion



---

# Plan & Solve
```
def plan_and_solve(task):
    """Simplified Plan & Solve algorithm"""

    # Phase 1: Planning
    plan = llm_create_plan(task)
    # plan = [step1, step2, step3, ...]

    # Phase 2: Execution
    step_results = []
    for step in plan:
        result = llm_execute_step(
            task=task,
            step=step,
            previous_results=step_results
        )
        step_results.append(result)

    # Aggregation
    final_answer = llm_aggregate(
        task=task,
        plan=plan,
        results=step_results
    )

    return final_answer
```


## When to Use Plan & Solve

Ideal Use Cases

✅ Structured problem solving

Agent creates detailed plan upfront
Executes steps sequentially
Each step builds on previous results
✅ Multi-step workflows

Clear dependency between steps
Benefits from upfront planning
Systematic execution required
✅ Complex calculations

Multi-stage mathematical problems
Data processing pipelines
Algorithm implementation
✅ Research and analysis tasks

Information gathering workflows
Systematic investigation
Sequential reasoning chains

## When NOT to Use Plan & Solve

❌ Dynamic environments → Use ReAct for adaptive planning 
❌ Tool-based workflows → Use ReAct or REWOO 
❌ Learning from failures → Use Reflexion 
❌ One-step tasks → Direct LLM call sufficient

---
# Reflexion


## When to Use Reflexion

Ideal Use Cases

✅ Problem-solving with trial and error

Agent attempts solution
Evaluates success/failure
Learns from mistakes
Tries again with improved approach
✅ Optimization tasks

Multiple attempts to find best solution
Each trial provides learning
Memory guides future strategies
Converges toward optimal approach
✅ Complex puzzles and challenges

Initial attempts may fail
Insights from failures inform next try
Persistent memory tracks what doesn’t work
Gradual refinement leads to solution
✅ Adaptive strategy development

Explores different approaches
Learns which strategies succeed
Builds knowledge base over trials
Applies lessons to new attempts

## When NOT to Use Reflexion

❌ One-shot tasks → Use Reflection or direct LLM ❌ No clear success/failure criteria → Hard to evaluate trials ❌ Cost-sensitive applications → Many trials = high cost ❌ Time-critical tasks → Multiple trials take time
