CREATE TABLE PRODCEOBJSTORE3 (
    ID INT PRIMARY KEY NOT NULL,
	RL_AccountNumber VARCHAR2(48 BYTE),
	RL_ApplicationNumber VARCHAR2(39 BYTE),
	RL_DocumentCategory VARCHAR2(90 BYTE),
	RL_ChannelName VARCHAR2(30 BYTE),
	RL_DateOfBirth DATE,
	RL_DateTimeReceived DATE,
	RL_DateTimeVerified DATE,
	DocumentTitle VARCHAR2(765 BYTE),
	RL_FirstName VARCHAR2(192 BYTE)
	RL_LastName VARCHAR2(192 BYTE),
	RL_QueueName VARCHAR2(90 BYTE),
	DateCreated DATE,
	DateLastModified DATE,
	LastModifier VARCHAR2(240 BYTE),
	MajorVersionNumber NUMBER(10,0) NOT NULL ENABLE
);