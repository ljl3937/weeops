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
from typing import Any, Optional

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

    def execute_selenium_action(self, action: dict[str, Any]):
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
        return res