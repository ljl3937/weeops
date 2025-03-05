#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Desc   : MG Selenium Env

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager  # Ensure this import is correct
from pydantic import Field
from metagpt.environment.base_env import Environment
from typing import Any, Optional, Dict
import re

# 添加LLMService类
class LLMService:
    """使用LLM进行页面元素定位的服务类"""
    
    def analyze_page(self, page_source: str, user_intent: str) -> Dict[str, Any]:
        """
        分析页面源码，根据用户意图返回元素定位策略
        
        Args:
            page_source: 页面HTML源码
            user_intent: 用户意图描述，如"搜索按钮"、"登录链接"等
            
        Returns:
            定位策略字典，如 {"by": By.ID, "value": "kw"}
        """
        # 这里是一个简化的实现，实际应用中应该调用LLM API
        # 对于常见的百度搜索场景，我们可以硬编码一些规则
        
        if "搜索" in user_intent and ("输入" in user_intent or "框" in user_intent):
            return {"by": By.ID, "value": "kw"}
        elif "搜索" in user_intent and "按钮" in user_intent:
            return {"by": By.ID, "value": "su"}
        
        # 如果没有匹配的规则，尝试从页面源码中提取可能的元素
        # 这里使用简单的正则表达式匹配，实际应用中应该使用更复杂的算法
        if "按钮" in user_intent:
            button_pattern = r'<button[^>]*id="([^"]*)"[^>]*>'
            matches = re.findall(button_pattern, page_source)
            if matches:
                return {"by": By.ID, "value": matches[0]}
        
        if "输入" in user_intent or "框" in user_intent:
            input_pattern = r'<input[^>]*id="([^"]*)"[^>]*>'
            matches = re.findall(input_pattern, page_source)
            if matches:
                return {"by": By.ID, "value": matches[0]}
        
        # 默认返回一个通用的XPath策略
        return {"by": By.XPATH, "value": f"//*[contains(text(), '{user_intent}')]"}

# 在 SeleniumEnv 类中新增方法
class SeleniumEnv(Environment):
    """Environment class for Selenium operations"""

    driver: webdriver.Chrome = Field(default=None, description="Selenium WebDriver instance")
    url: str = Field(default="", description="Current URL of the browser")

    def __init__(self, **data: Any):
        super().__init__(**data)
        chrome_options = Options()
        # chrome_options.add_argument("--headless")  # Run in headless mode
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

    def reset(self, *, seed: Optional[int] = None, options: Optional[dict[str, Any]] = None) -> tuple[dict[str, Any], dict[str, Any]]:
        super().reset(seed=seed, options=options)
        self.driver.quit()
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=Options())
        obs = self._get_obs()
        return obs, {}

    def _get_obs(self) -> dict[str, Any]:
        obs = {
            "url": self.driver.current_url,
            "title": self.driver.title,
            "page_source": self.driver.page_source
        }
        return obs

    def observe(self, obs_params: Optional[dict[str, Any]] = None) -> Any:
        obs_type = obs_params.get("obs_type", "NONE")
        if obs_type == "NONE":
            pass
        elif obs_type == "GET_URL":
            obs = self.driver.current_url
        elif obs_type == "GET_TITLE":
            obs = self.driver.title
        elif obs_type == "GET_PAGE_SOURCE":
            obs = self.driver.page_source
        return obs

    def step(self, action: dict[str, Any]) -> tuple[dict[str, Any], float, bool, bool, dict[str, Any]]:
        action_type = action.get("action_type", "NONE")
        res = None
        if action_type == "NONE":
            pass
        elif action_type == "NAVIGATE":
            url = action.get("url")
            self.driver.get(url)
            res = self._get_obs()
        elif action_type == "FIND_ELEMENT":
            by = action.get("by")
            value = action.get("value")
            element = self.driver.find_element(by, value)
            res = {"element": element}
        elif action_type == "CLICK_ELEMENT":
            element = action.get("element")
            element.click()
            res = self._get_obs()
        elif action_type == "SEND_KEYS":
            element = action.get("element")
            keys = action.get("keys")
            element.send_keys(keys)
            res = self._get_obs()
        elif action_type == "GET_TITLE":
            res = self.driver.title
        elif action_type == "QUIT":
            self.driver.quit()
            res = {}
        return res, 1.0, False, False, {"res": res}

    def find_element_with_llm(self, page_source: str, user_intent: str) -> dict:
        """使用大模型根据用户意图定位页面元素"""
        # 调用大模型服务
        llm_service = LLMService()
        localization_strategy = llm_service.analyze_page(
            page_source=page_source,
            user_intent=user_intent
        )
        
        # 使用定位策略查找元素
        element = self.driver.find_element(
            by=localization_strategy["by"],
            value=localization_strategy["value"]
        )
        
        return {"element": element}

    def execute_selenium_action(self, action: dict[str, Any]):
        action_type = action.get("action_type", "NONE")  # 需要先获取action_type
        res = None
        
        # 新增LLM元素定位分支
        if action_type == "FIND_ELEMENT_WITH_LLM":
            page_source = self.driver.page_source
            user_intent = action.get("user_intent")
            element = self.find_element_with_llm(page_source, user_intent)
            return {"element": element}
        
        # 保留原有基础操作分支
        if action_type == "NONE":
            pass
        elif action_type == "NAVIGATE":
            url = action.get("url")
            self.driver.get(url)
            res = self._get_obs()
        elif action_type == "FIND_ELEMENT":
            by = action.get("by")
            value = action.get("value")
            element = self.driver.find_element(by, value)
            res = {"element": element}
        elif action_type == "CLICK_ELEMENT":
            element = action.get("element")
            element.click()
            res = self._get_obs()
        elif action_type == "SEND_KEYS":
            element = action.get("element")
            keys = action.get("keys")
            element.send_keys(keys)
            res = self._get_obs()
        elif action_type == "GET_TITLE":
            res = self.driver.title
        elif action_type == "QUIT":
            self.driver.quit()
            res = {}
        return res