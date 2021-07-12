import React from 'react';
import { Alert } from 'antd';
import { useGetMlFeatureTableQuery } from '../../../../graphql/mlFeatureTable.generated';
import { EntityProfile } from '../../../shared/EntityProfile';
import { MlFeatureTable, MlFeature, MlPrimaryKey, EntityType } from '../../../../types.generated';
import MLFeatureTableHeader from './MLFeatureTableHeader';
import { Message } from '../../../shared/Message';
import { Ownership as OwnershipView } from '../../shared/Ownership';
import { useEntityRegistry } from '../../../useEntityRegistry';
import analytics, { EventType } from '../../../analytics';
import { notEmpty } from '../../shared/utils';
import MlFeatureTableSchema from './schema/MlFeatureTableSchema';
import SourcesView from './Sources';

export enum TabType {
    Features = 'Features',
    Sources = 'Sources',
    Ownership = 'Ownership',
}

/**
 * Responsible for display the MLFeatureTable Page
 */
export const MLFeatureTableProfile = ({ urn }: { urn: string }): JSX.Element => {
    const entityRegistry = useEntityRegistry();
    const { loading, error, data } = useGetMlFeatureTableQuery({ variables: { urn } });

    if (error || (!loading && !error && !data)) {
        return <Alert type="error" message={error?.message || 'Entity failed to load'} />;
    }
    const getHeader = (mlFeatureTable: MlFeatureTable) => <MLFeatureTableHeader mlFeatureTable={mlFeatureTable} />;

    const getTabs = ({ ownership, featureTableProperties }: MlFeatureTable) => {
        const sources: Array<MlFeature | MlPrimaryKey> =
            featureTableProperties && (featureTableProperties?.mlFeatures || featureTableProperties?.mlPrimaryKeys)
                ? [
                      ...(featureTableProperties?.mlFeatures || []),
                      ...(featureTableProperties?.mlPrimaryKeys || []),
                  ].filter(notEmpty)
                : [];

        return [
            {
                name: TabType.Features,
                path: TabType.Features.toLowerCase(),
                content: <MlFeatureTableSchema sources={sources} />,
            },
            {
                name: TabType.Sources,
                path: TabType.Sources.toLowerCase(),
                content: <SourcesView sources={sources} />,
            },
            {
                name: TabType.Ownership,
                path: TabType.Ownership.toLowerCase(),
                content: (
                    <OwnershipView
                        owners={(ownership && ownership.owners) || []}
                        lastModifiedAt={(ownership && ownership.lastModified?.time) || 0}
                    />
                ),
            },
        ];
    };

    return (
        <>
            {loading && <Message type="loading" content="Loading..." style={{ marginTop: '10%' }} />}
            {data && data.mlFeatureTable && (
                <EntityProfile
                    titleLink={`/${entityRegistry.getPathName(EntityType.MlfeatureTable)}/${urn}`}
                    title={data.mlFeatureTable?.name || ''}
                    tabs={getTabs(data.mlFeatureTable as MlFeatureTable)}
                    header={getHeader(data.mlFeatureTable as MlFeatureTable)}
                    onTabChange={(tab: string) => {
                        analytics.event({
                            type: EventType.EntitySectionViewEvent,
                            entityType: EntityType.MlfeatureTable,
                            entityUrn: urn,
                            section: tab,
                        });
                    }}
                />
            )}
        </>
    );
};
