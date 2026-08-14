import sys

content = open('backend/roadmaps/engine.py').read()
content = content.replace(
'''
            if opp:
                source_type = "opportunity"
                opp_id = opp.id
            else:
                # In current schema AgentRecommendation and WorkflowRecommendation link to Opportunity.
                # However, just to strictly follow the prompt instruction to use *whichever* of the three exists
                # for the system... we need to search for them if no direct opportunity matches (e.g. if they somehow
                # link through a different structure or were created detached in test data).
                # Actually, AgentRecommendation and WorkflowRecommendation don't have ai_system_id directly, they have opportunity_id.
                # Thus if there's no opportunity_id for this ai_system_id, there logically can be no agent/workflow recs
                # for this ai_system_id because they only join through Opportunity.
                #
                # Let's perform a broad search across all opportunities that might be related, or fallback to known gap.

                # We will check if there is an opportunity that has an AgentRecommendation
                ar_stmt = select(AgentRecommendation).join(Opportunity).where(Opportunity.ai_system_id == system.id).limit(1)
                ar_result = await db_session.execute(ar_stmt)
                ar = ar_result.scalar_one_or_none()

                if ar:
                    source_type = "agent_recommendation"
                    ar_id = ar.id
                else:
                    wr_stmt = select(WorkflowRecommendation).join(Opportunity).where(Opportunity.ai_system_id == system.id).limit(1)
                    wr_result = await db_session.execute(wr_stmt)
                    wr = wr_result.scalar_one_or_none()

                    if wr:
                        source_type = "workflow_recommendation"
                        wr_id = wr.id
''',
'''
            if opp:
                source_type = "opportunity"
                opp_id = opp.id
            else:
                # As noted, AgentRecommendation and WorkflowRecommendation don't have ai_system_id directly, they have opportunity_id.
                # Thus if there's no opportunity_id for this ai_system_id, there logically can be no agent/workflow recs
                # for this ai_system_id because they only join through Opportunity.
                pass
'''
)
open('backend/roadmaps/engine.py', 'w').write(content)
