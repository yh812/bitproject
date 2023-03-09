package com.vam.model;

import lombok.Data;

@Data
public class OrderCancelDTO {
	
private String memberId;
	
	private String orderId;
	
	private String keyword;
	
	private int amount;
	
	private int pageNum;

}
