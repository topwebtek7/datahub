import React, { useCallback, useState, useEffect } from 'react';
import { Button, Pagination, Typography } from 'antd';
import styled from 'styled-components';
import { FetchResult } from '@apollo/client';
import { Message } from '../../../../shared/Message';
import { useGetDatasetSchemaVersionsLazyQuery, UpdateDatasetMutation } from '../../../../../graphql/dataset.generated';
import {
    Schema,
    SchemaMetadata,
    EditableSchemaMetadata,
    EditableSchemaMetadataUpdate,
    GlobalTagsUpdate,
    EditableSchemaFieldInfo,
    EditableSchemaFieldInfoUpdate,
    EntityType,
    UsageQueryResult,
} from '../../../../../types.generated';
import {
    convertEditableSchemaMetadataForUpdate,
    diffJson,
    fieldPathSortAndParse,
    ExtendedSchemaFields,
} from '../../../shared/utils';
import { convertTagsForUpdate } from '../../../../shared/tags/utils/convertTagsForUpdate';
import SchemaTable from './SchemaTable';
import analytics, { EventType, EntityActionType } from '../../../../analytics';

const SchemaContainer = styled.div`
    margin-bottom: 100px;
`;
const ViewRawButtonContainer = styled.div<{ padding?: string }>`
    display: flex;
    justify-content: flex-end;
    ${(props) => (props.padding ? 'padding-bottom: 16px;' : '')}
`;

const ShowVersionButton = styled(Button)`
    margin-right: 10px;
`;
const PaginationContainer = styled(Pagination)`
    padding-top: 5px;
    margin-right: 15px;
`;
const SummaryContainer = styled.div`
    margin-top: -32px;
    margin-bottom: 16px;
    padding-left: 10px;
    & ul {
        padding-inline-start: 30px;
        margin-top: 5px;
    }
`;
const SummarySubHeader = styled(Typography.Text)``;

export type Props = {
    urn: string;
    usageStats?: UsageQueryResult | null;
    schema?: SchemaMetadata | Schema | null;
    pastSchemaMetadata?: SchemaMetadata | null;
    editableSchemaMetadata?: EditableSchemaMetadata | null;
    updateEditableSchema: (
        update: EditableSchemaMetadataUpdate,
    ) => Promise<FetchResult<UpdateDatasetMutation, Record<string, any>, Record<string, any>>>;
};

export default function SchemaView({
    urn,
    schema,
    pastSchemaMetadata,
    editableSchemaMetadata,
    updateEditableSchema,
    usageStats,
}: Props) {
    const totalVersions = pastSchemaMetadata?.aspectVersion || 0;
    const [showRaw, setShowRaw] = useState(false);
    const [diffSummary, setDiffSummary] = useState({ added: 0, removed: 0, updated: 0, schemaRawUpdated: false });
    const [showVersions, setShowVersions] = useState(false);
    const [currentVersion, setCurrentVersion] = useState(totalVersions);
    const [rows, setRows] = useState<Array<ExtendedSchemaFields>>([]);
    const [schemaRawDiff, setSchemaRawDiff] = useState<string>('');
    const [getSchemaVersions, { loading, error, data: schemaVersions }] = useGetDatasetSchemaVersionsLazyQuery({
        fetchPolicy: 'no-cache',
    });

    const getRawSchema = (schemaValue) => {
        try {
            return JSON.stringify(JSON.parse(schemaValue), null, 2);
        } catch (e) {
            return schemaValue;
        }
    };

    const updateDiff = useCallback(
        (currentSchema?: SchemaMetadata | Schema | null, pastSchema?: SchemaMetadata | null) => {
            const { fields, added, removed, updated } = fieldPathSortAndParse(
                currentSchema?.fields,
                pastSchema?.fields,
                !showVersions,
            );
            const currentSchemaRaw =
                currentSchema?.platformSchema?.__typename === 'TableSchema'
                    ? getRawSchema(currentSchema.platformSchema.schema)
                    : '';
            if (showVersions) {
                const pastSchemaRaw =
                    pastSchema?.platformSchema?.__typename === 'TableSchema'
                        ? getRawSchema(pastSchema.platformSchema.schema)
                        : '';
                setSchemaRawDiff(diffJson(pastSchemaRaw, currentSchemaRaw));
                setDiffSummary({ added, removed, updated, schemaRawUpdated: currentSchemaRaw === pastSchemaRaw });
            } else {
                setSchemaRawDiff(currentSchemaRaw);
            }
            setRows(fields);
        },
        [showVersions],
    );

    useEffect(() => {
        if (!loading && !error && schemaVersions) {
            updateDiff(schemaVersions.dataset?.schemaMetadata, schemaVersions.dataset?.pastSchemaMetadata);
        }
    }, [schemaVersions, loading, error, updateDiff]);

    useEffect(() => {
        updateDiff(schema, pastSchemaMetadata);
    }, [schema, pastSchemaMetadata, updateDiff]);

    const updateSchema = (newFieldInfo: EditableSchemaFieldInfoUpdate, record?: EditableSchemaFieldInfo) => {
        let existingMetadataAsUpdate = convertEditableSchemaMetadataForUpdate(editableSchemaMetadata);

        if (existingMetadataAsUpdate.editableSchemaFieldInfo.some((field) => field.fieldPath === record?.fieldPath)) {
            // if we already have a record for this field, update the record
            existingMetadataAsUpdate = {
                editableSchemaFieldInfo: existingMetadataAsUpdate.editableSchemaFieldInfo.map((fieldUpdate) => {
                    if (fieldUpdate.fieldPath === record?.fieldPath) {
                        return newFieldInfo;
                    }
                    return fieldUpdate;
                }),
            };
        } else {
            // otherwise add a new record
            existingMetadataAsUpdate.editableSchemaFieldInfo.push(newFieldInfo);
        }
        return updateEditableSchema(existingMetadataAsUpdate);
    };

    const onUpdateTags = (update: GlobalTagsUpdate, record?: EditableSchemaFieldInfo) => {
        if (!record) return Promise.resolve();
        analytics.event({
            type: EventType.EntityActionEvent,
            actionType: EntityActionType.UpdateSchemaTags,
            entityType: EntityType.Dataset,
            entityUrn: urn,
        });
        const newFieldInfo: EditableSchemaFieldInfoUpdate = {
            fieldPath: record?.fieldPath,
            description: record?.description,
            globalTags: update,
        };
        return updateSchema(newFieldInfo, record);
    };

    const onUpdateDescription = (
        updatedDescription: string,
        record?: EditableSchemaFieldInfo | ExtendedSchemaFields,
    ) => {
        if (!record) return Promise.resolve();
        analytics.event({
            type: EventType.EntityActionEvent,
            actionType: EntityActionType.UpdateSchemaDescription,
            entityType: EntityType.Dataset,
            entityUrn: urn,
        });
        const newFieldInfo: EditableSchemaFieldInfoUpdate = {
            fieldPath: record?.fieldPath,
            description: updatedDescription,
            globalTags: { tags: convertTagsForUpdate(record?.globalTags?.tags || []) },
        };
        return updateSchema(newFieldInfo, record as EditableSchemaFieldInfo);
    };

    const onVersionChange = (version) => {
        if (version === null) {
            return;
        }
        setCurrentVersion(version);
        if (version === totalVersions) {
            updateDiff(schema, pastSchemaMetadata);
            return;
        }
        getSchemaVersions({
            variables: {
                urn,
                version1: version - totalVersions,
                version2: version - totalVersions - 1,
            },
        });
    };

    return (
        <SchemaContainer>
            {loading && <Message type="loading" content="Loading..." style={{ marginTop: '30%' }} />}
            <ViewRawButtonContainer padding={!showVersions ? 'true' : undefined}>
                {totalVersions > 0 &&
                    (!showVersions ? (
                        <ShowVersionButton onClick={() => setShowVersions(true)}>Version History</ShowVersionButton>
                    ) : (
                        <>
                            <ShowVersionButton
                                onClick={() => {
                                    setShowVersions(false);
                                    setCurrentVersion(totalVersions);
                                }}
                            >
                                Back
                            </ShowVersionButton>
                            <PaginationContainer
                                simple
                                size="default"
                                defaultCurrent={totalVersions}
                                defaultPageSize={1}
                                total={totalVersions}
                                onChange={onVersionChange}
                                current={currentVersion}
                            />
                        </>
                    ))}
                {schema?.platformSchema?.__typename === 'TableSchema' && schema?.platformSchema?.schema?.length > 0 && (
                    <Button onClick={() => setShowRaw(!showRaw)}>{showRaw ? 'Tabular' : 'Raw'}</Button>
                )}
            </ViewRawButtonContainer>
            {showRaw ? (
                <Typography.Text data-testid="schema-raw-view">
                    <pre>
                        <code>{schemaRawDiff}</code>
                    </pre>
                </Typography.Text>
            ) : (
                rows.length > 0 && (
                    <>
                        {showVersions && (
                            <SummaryContainer>
                                <Typography.Title level={5}>Summary</Typography.Title>
                                <SummarySubHeader>{`Comparing version ${currentVersion} to version ${
                                    currentVersion - 1
                                }`}</SummarySubHeader>
                                <ul>
                                    {diffSummary.added ? (
                                        <li>
                                            <Typography.Text>{`${diffSummary.added} column${
                                                diffSummary.added > 1 ? 's were' : ' was'
                                            } added`}</Typography.Text>
                                        </li>
                                    ) : null}
                                    {diffSummary.removed ? (
                                        <li>
                                            <Typography.Text>{`${diffSummary.removed} column${
                                                diffSummary.removed > 1 ? 's were' : ' was'
                                            } removed`}</Typography.Text>
                                        </li>
                                    ) : null}
                                    {diffSummary.updated ? (
                                        <li>
                                            <Typography.Text>{`${diffSummary.updated} description${
                                                diffSummary.updated > 1 ? 's were' : ' was'
                                            } updated`}</Typography.Text>
                                        </li>
                                    ) : null}
                                </ul>
                            </SummaryContainer>
                        )}
                        <SchemaTable
                            rows={rows}
                            editMode={!showVersions}
                            onUpdateDescription={onUpdateDescription}
                            onUpdateTags={onUpdateTags}
                            editableSchemaMetadata={editableSchemaMetadata}
                            usageStats={usageStats}
                        />
                    </>
                )
            )}
        </SchemaContainer>
    );
}
