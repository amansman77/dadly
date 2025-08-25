"""Chat service using LangChain."""

import uuid
from datetime import datetime
from typing import List, Optional, Dict, Any
from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage, AIMessage, SystemMessage
from langchain.memory import ConversationBufferMemory
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.chains import LLMChain
from langchain.callbacks import LangChainTracer

from config import settings
from models.chat import ChatMessage, MessageRole, ChatResponse, Conversation


class ChatService:
    """Chat service using LangChain."""
    
    def __init__(self):
        """Initialize chat service."""
        # For testing, use a mock LLM if API key is not valid
        if settings.openai_api_key.startswith("sk-test"):
            self.llm = None
        else:
            self.llm = ChatOpenAI(
                model="gpt-3.5-turbo",
                temperature=0.7,
                api_key=settings.openai_api_key,
            )
        
        # Initialize LangSmith tracing (only if API key is provided)
        if (settings.langchain_tracing_v2 and 
            settings.langchain_api_key and 
            settings.langchain_api_key != "" and
            not settings.langchain_api_key.startswith("test")):
            try:
                # Set environment variable for LangSmith
                import os
                os.environ["LANGCHAIN_API_KEY"] = settings.langchain_api_key
                os.environ["LANGCHAIN_PROJECT"] = settings.langchain_project
                os.environ["LANGCHAIN_TRACING_V2"] = "true"
                
                self.tracer = LangChainTracer(
                    project_name=settings.langchain_project
                )
                print(f"LangSmith tracing enabled for project: {settings.langchain_project}")
            except Exception as e:
                print(f"LangSmith tracing failed: {e}")
                self.tracer = None
        else:
            print(f"LangSmith tracing disabled. API key: {settings.langchain_api_key[:10] if settings.langchain_api_key else 'None'}...")
            self.tracer = None
        
        # Conversation memories (in production, use Redis or database)
        self._memories: Dict[str, ConversationBufferMemory] = {}
        
        # System prompt for Dadly
        self.system_prompt = """당신은 'Dadly'라는 가족 기록 아카이브 서비스의 AI 어시스턴트입니다.

Dadly는 아빠가 남긴 기록과 이야기를 가족과 함께 나누고, 시간이 흘러도 잊히지 않도록 보존하는 서비스입니다.

당신의 역할:
1. 가족의 추억과 기록에 대해 따뜻하고 공감적인 대화를 나눕니다
2. 아빠의 기록을 찾거나 정리하는 것을 도와줍니다
3. 가족의 소중한 순간들을 기억하고 보존하는 방법을 제안합니다
4. 감정적이고 따뜻한 톤을 유지하면서 실용적인 도움을 제공합니다

답변할 때는:
- 항상 따뜻하고 공감적인 톤을 유지하세요
- 가족의 소중함을 강조하세요
- 실용적이면서도 감정적인 조언을 제공하세요
- 한국어로 답변하세요"""
        
        # Create prompt template
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", self.system_prompt),
            MessagesPlaceholder(variable_name="chat_history"),
            ("human", "{input}")
        ])
        
        # Create LLM chain (only if LLM is available)
        if self.llm is not None:
            self.chain = LLMChain(
                llm=self.llm,
                prompt=self.prompt,
                verbose=settings.debug
            )
        else:
            self.chain = None
    
    def _get_memory(self, conversation_id: str) -> ConversationBufferMemory:
        """Get or create conversation memory."""
        if conversation_id not in self._memories:
            self._memories[conversation_id] = ConversationBufferMemory(
                memory_key="chat_history",
                return_messages=True
            )
        return self._memories[conversation_id]
    
    def _format_messages_for_memory(self, messages: List[ChatMessage]) -> List:
        """Format chat messages for LangChain memory."""
        formatted_messages = []
        for msg in messages:
            if msg.role == MessageRole.USER:
                formatted_messages.append(HumanMessage(content=msg.content))
            elif msg.role == MessageRole.ASSISTANT:
                formatted_messages.append(AIMessage(content=msg.content))
            elif msg.role == MessageRole.SYSTEM:
                formatted_messages.append(SystemMessage(content=msg.content))
        return formatted_messages
    
    async def chat(
        self, 
        message: str, 
        conversation_id: Optional[str] = None,
        user_id: Optional[str] = None
    ) -> ChatResponse:
        """Process chat message and return response."""
        # Generate conversation ID if not provided
        if not conversation_id:
            conversation_id = str(uuid.uuid4())
        
        # Get conversation memory
        memory = self._get_memory(conversation_id)
        
        # Run the chain
        try:
            if self.llm is None:
                # Mock response for testing
                response_text = f"안녕하세요! Dadly AI 어시스턴트입니다. '{message}'에 대한 답변을 드리겠습니다. 현재는 테스트 모드로 실행 중입니다. 실제 OpenAI API 키를 설정하시면 더 정교한 대화가 가능합니다."
            else:
                response = await self.chain.ainvoke({
                    "input": message,
                    "chat_history": memory.chat_memory.messages
                })
                response_text = response["text"] if isinstance(response, dict) else str(response)
            
            # Generate message ID
            message_id = str(uuid.uuid4())
            
            # Create response
            chat_response = ChatResponse(
                message=response_text.strip(),
                conversation_id=conversation_id,
                message_id=message_id,
                timestamp=datetime.utcnow()
            )
            
            # Save to memory
            memory.chat_memory.add_user_message(message)
            memory.chat_memory.add_ai_message(response_text.strip())
            
            return chat_response
            
        except Exception as e:
            # Handle errors gracefully
            error_message = "죄송합니다. 일시적인 오류가 발생했습니다. 잠시 후 다시 시도해주세요."
            if settings.debug:
                error_message += f" (Error: {str(e)})"
            
            return ChatResponse(
                message=error_message,
                conversation_id=conversation_id,
                message_id=str(uuid.uuid4()),
                timestamp=datetime.utcnow()
            )
    
    def get_conversation_history(self, conversation_id: str) -> List[ChatMessage]:
        """Get conversation history."""
        memory = self._get_memory(conversation_id)
        messages = []
        
        for msg in memory.chat_memory.messages:
            if isinstance(msg, HumanMessage):
                messages.append(ChatMessage(
                    role=MessageRole.USER,
                    content=msg.content,
                    timestamp=datetime.utcnow()  # In production, get actual timestamp
                ))
            elif isinstance(msg, AIMessage):
                messages.append(ChatMessage(
                    role=MessageRole.ASSISTANT,
                    content=msg.content,
                    timestamp=datetime.utcnow()  # In production, get actual timestamp
                ))
        
        return messages
    
    def clear_conversation(self, conversation_id: str) -> bool:
        """Clear conversation memory."""
        if conversation_id in self._memories:
            del self._memories[conversation_id]
            return True
        return False


# Global chat service instance
chat_service = ChatService()
